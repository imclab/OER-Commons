var vp = vp || {};

(function() {

  vp.initVideoPlayer = function (container, videoURL, contentType, caption) {
      var instance = [{
          container: container,
          options: {
            video: {
              sources: [
                {
                  src: videoURL,
                  type: contentType
                }
              ]
            },
            templates: {
                videoPlayer: {
                    forceCache: true,
                    href: "/media/javascripts/videoPlayer/html/videoPlayer_template.html"
                }
            },
            listeners:{
                onReady: function (videoPlayer) {
                    videoPlayer.container.append($(caption));
                }
            } 
          }
        }];

        fluid.videoPlayer.makeEnhancedInstances(instance, uiOptions.relay);
    };
})();

