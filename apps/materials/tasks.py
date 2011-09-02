from __future__ import absolute_import

from celery.decorators import task
from django.conf import settings
from django.utils.encoding import smart_str
from django.utils.hashcompat import md5_constructor
from haystack_scheduled.indexes import Indexed
from sorl.thumbnail.shortcuts import delete
from utils import update_item
import os
import shlex
import subprocess
import sys
import urllib
import httplib


@task
def reindex_microsite_topic(topic):
    from haystack.query import SearchQuerySet

    objects = set()

    # get all objects from this topic and all objects with this topic's keywords
    query = "indexed_topics:%s" % topic.id
    for result in SearchQuerySet().narrow(query).load_all():
        objects.add(result.object)

    topic_keywords = topic.keywords.values_list("slug", flat=True)
    microsite_keywords = topic.microsite.keywords.values_list("slug", flat=True)
    if topic_keywords and microsite_keywords:
        query = SearchQuerySet()
        query = query.narrow("keywords(%s)" % " OR ".join(["%s" % kw for kw in topic_keywords]))
        query = query.narrow("keywords(%s)" % " OR ".join(["%s" % kw for kw in microsite_keywords]))
        for result in query.load_all():
            objects.add(result.object)

    for instance in objects:
        if isinstance(instance, Indexed):
            instance.reindex()


class TimeoutError(Exception):

    def __init__(self, value="Timed Out"):
        self.value = value

    def __str__(self):
        return repr(self.value)


def timeout(function=None, timeout_duration=10, default=None):

    def raise_timeout(signum, frame):
        raise TimeoutError()

    def wrapper(func):

        def wrapped(*args, **kwargs):
            import signal
            signal.signal(signal.SIGALRM, raise_timeout)
            signal.alarm(timeout_duration)
            try:
                return func(*args, **kwargs)
            except TimeoutError:
                return default
            finally:
                signal.alarm(0)

        return wrapped

    if function:
        return wrapper(function)

    return wrapper


def get_url_status_code(url):
    url = url.strip()
    url = urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
    if not url:
        return

    try:
        host = url.split('/')[2]
        path = "/" + "/".join(url.split('/')[3:])
    except:
        return None

    @timeout(timeout_duration=60)
    def get_status(host, path):
        try:
            conn = httplib.HTTPConnection(host)
            conn.request("HEAD", path)
            response = conn.getresponse()
            return response.status
        except TimeoutError:
            raise
        except:
            return None

    status_code = get_status(host, path)

    return status_code


def check_url_status(item):
    status_code = get_url_status_code(item.url)

    if item.http_status != status_code:
        update_item(item, http_status=status_code)
        if isinstance(item, Indexed):
            item.reindex()


def update_screenshot(item):
    url = item.url

    url = url.strip()
    url = urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
    if not url:
        return

    if item.http_status != 200:
        if item.screenshot:
            delete(item.screenshot)
            update_item(item, screenshot=None)
        return

    url_hash = md5_constructor(smart_str(url)).hexdigest()
    filename = "%s-%i-%s.png" % (item._meta.object_name.lower(), item.id, url_hash)
    filename = os.path.join(item.screenshot.field.get_directory_name(), filename)
    if item.screenshot:
        try:
            # check that the file actually exists
            item.screenshot.size
            if item.screenshot.name == filename:
                return
            else:
                delete(item.screenshot)
                update_item(item, screenshot=None)
        except OSError:
            pass

    full_path = os.path.join(settings.MEDIA_ROOT, filename)
    dirname = os.path.dirname(full_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    width = 1024
    height = 768

    executable = settings.WEBKIT2PNG_EXECUTABLE % dict(filename=full_path,
                                                       url='"%s"' % url.replace('"', '\\"'),
                                                       width=width,
                                                       height=height)
    if isinstance(executable, unicode):
        executable = executable.encode(sys.getfilesystemencoding())
    args = shlex.split(executable)

    @timeout(timeout_duration=60*2)
    def fetch_screenshot(args):
        p = subprocess.Popen(args)
        try:
            p.wait()
            return 1
        except TimeoutError:
            p.kill()
            raise
        finally:
            try:
                p.terminate()
            except OSError:
                pass
        return None

    result = fetch_screenshot(args)
    if result:
        if os.path.exists(full_path):
            update_item(item, screenshot=filename)
    else:
        update_item(item, screenshot=None)
