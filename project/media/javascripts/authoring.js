oer.authoring = {};

oer.authoring.init_edit_lesson = function() {
  var $form = $("#edit-lesson-form");

  var $student_levels = $form.find("div.student-levels");
  $student_levels.find("a").click(function(e) {
      e.preventDefault();
      $student_levels.children("ul").hide();
      $(this).hide();
      $student_levels.find("div.field ul").fadeIn();
  });


  var autosave = function() {
    var serialized = $form.data("serialized");
    var current_serialized = $form.serialize();
    if (serialized === undefined) {
        $form.data("serialized", current_serialized);
    } else {
        if (serialized !== current_serialized) {
            $form.submit();
            $form.data("serialized", current_serialized);
        }
    }
    setTimeout(autosave, 10000);
  };

  autosave();

  var $goals_field = $form.find("div.field.goals");
  var $goals_list = $goals_field.find("ul");
  $goals_field.find("a").click(function(e) {
      e.preventDefault();
      var $item = $goals_list.find("li").eq(0).clone();
      $item.find("input").val("").removeAttr("id");
      $item.appendTo($goals_list);
  });

  $.validator.addMethod("null", function(value, element) {
      return true;
  }, "");
  var validator = $form.validate({
    rules: {
        title: "required",
        summary: "required",
        subjects: "required",
        goals: "null"
    },
    submitHandler: function(form) {
        console.log(form);
        $.post($form.attr("action"), $form.serialize(), function(response) {
            if (response.status === "success") {
                oer.status_message.success(response.message, true);
            } else if (response.status === "error") {
                console.log(response.errors);
                validator.showErrors(response.errors);
            }
        });
    }
  });

  var $image_widget = $form.find("div.image");
  var $image = $image_widget.find("img");
  var $image_upload = $image_widget.find("a.upload");
  var $image_remove = $image_widget.find("a.remove");
  $image_upload.upload({
        action: $image_upload.attr("href"),
        onComplete: function(response) {
            response = $.parseJSON(response);
            if (response.status === "error") {
                oer.status_message.error(response.message, true);
            } else if (response.status === "success") {
                $image.attr("src", response.url);
                $image_remove.show();
            }
            $image_widget.removeClass("loading");
            $image.show();
        },
        onSubmit: function() {
            $image_widget.addClass("loading");
            $image.hide();
        }
    });
  $image_remove.click(function(e) {
      e.preventDefault();
      $image.attr("src", "http://placehold.it/220x150/dddddd/333333&text=No%20image");
      $image_remove.hide();
      $.post($image_remove.attr("href"), function(response) {
          oer.status_message.success(response.message, true);
      });
  });

};