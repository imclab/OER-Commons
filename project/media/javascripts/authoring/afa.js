var afa = afa || {};

(function() {

  afa.AfAProperties = {
      mouseA11y: {
          name: "is-mouse-accessible",
          type: "boolean",
          selector: ".mouse-access",
          summaryfunc: "afa.checkA11y"
      },
      kbdA11y: {
          name: "is-keyboard-accessible",
          type: "boolean",
          selector: ".kbd-access",
          summaryfunc: "afa.checkA11y"
      },
      dispTrans: {
          name: "is-display-transformable",
          type: "vocabulary",
          values: ["font-size", "font-face", "foreground-colour", "background-colour"],
          selector: ".disp-trans",
          summaryfunc: "afa.checkDispTrans"
      },
      ebook: {
          name: "has-ebook",
          type: "boolean",
          selector: ".ebook",
          summaryfunc: "afa.checkEbook"
      },
      colourCode: {
          name: "uses-colour-coding ",
          type: "unknown",
          selector: ".colour-coding",
          summaryfunc: "afa.unknown"
      },
      hazard: {
          name: "has-hazard ",
          type: "unknown",
          selector: ".hazard",
          summaryfunc: "afa.unknown"
      },
      altText: {
        name: "has-alt-text",
        type: "boolean",
        selector: ".alt-text",
        summaryfunc: "afa.checkImgProp"
      },
      audioAdapt: {
        name: "has-audio-representation",
        type: "boolean",
        selector: ".audio-adapt",
        summaryfunc: "afa.checkImgProp"
      },
      imgLongDesc: {
        name: "has-long-description",
        type: "boolean",
        selector: ".img-long-desc",
        summaryfunc: "afa.checkImgProp"
      }
  };

  // Propsed structure for the mapping btw each AfA property status and its tooltip text
  var tooltipTextMapping = {
    mouseA11y: {
      green: "It is possible to operate the resource using the mouse only",
      yellow: "It may or may not be possible to operate parts of the resource using the mouse only",
      red: "It is not possible to operate the resource using the mouse only",
      grey: "Cannot determine whether it is possible to operate the resource using the mouse only"
    },
    kbdA11y: {
      green: "It is possible to operate the resource using the keyboard only",
      yellow: "It may or may not be possible to operate parts of the resource using the keyboard only",
      red: "It is not possible to operate the resource using the keyboard only",
      grey: "Cannot determine whether it is possible to operate the resource using the keyboard only"
    },
    dispTrans: {
      green: "green text for disp-trans",
      yellow: "yellow text for disp-trans",
      red: "red text for disp-trans",
      grey: "grey text for disp-trans"
    },
    ebook: {
      green: "green text for ebook",
      yellow: "yellow text for ebook",
      red: "red text for ebook",
      grey: "grey text for ebook"
    },
    colourCode: {
      grey: "grey text for colourCode"
    },
    hazard: {
      grey: "grey text for hazard"
    },
    altText: {
      green: "green text for img-alt",
      yellow: "yellow text for img-alt",
      red: "red text for img-alt",
      grey: "grey text for img-alt"
    },
    audioAdapt: {
      green: "green text for audioAdapt",
      yellow: "yellow text for audioAdapt",
      red: "red text for audioAdapt",
      grey: "grey text for audioAdapt"
    },
    imgLongDesc: {
      green: "green text for imgLongDesc",
      yellow: "yellow text for imgLongDesc",
      red: "red text for imgLongDesc",
      grey: "grey text for imgLongDesc"
    }
  };

  afa.buildTooltipContent = function (string) {
      return "<ul><li>"+string+"</li></ul>"
  };

  afa.updateUI = function (selector, level, tooltipText) {
    $(".afa-summary "+selector).addClass(level);
  
    fluid.tooltip(".afa-summary " + selector, {
      content: function () {
          // TODO: The construction of the tooltip html will have to move earlier, since it
          //       will be more specific to the different properties
          return afa.buildTooltipContent(tooltipText);
      }
    });
  
  }

  /**
   * Each of these functions below check on one AfA property
   * @param itemName: the defined name to identify having alt text on the OER content
   *        itemProperty: the properties, including the used terminology or css selector, that 
   *                      associate with the AfA item
   * @returns A json string in the structure of 
   *          {
   *            "description": [string],
   *            "tooltipText": [string]
   *          }
   */
  
  /**
   * Check on AfA properties specifically used by <img>, for example, has-alt-text
   */
  afa.checkImgProp = function (itemName, itemProperty) {
    var total = $(".oer-container img").length;
    var yes = $(".oer-container img").parent().children("meta[itemprop='" + itemProperty.name + "'][content='true']").length;
    var no = $(".oer-container img").parent().children("meta[itemprop='" + itemProperty.name + "'][content='false']").length;
      
    var level = (yes === 0 && no === 0 && total !== 0 ? "grey" : (yes === total && total === 0 ? "green" : (no === total ? "red" : "yellow")));
    
    return {
      level: level,
      // TODO: Constructing tooltip text will become more complex, as we will combine multiple strings
      tooltipText: tooltipTextMapping[itemName][level] + "; " + level
    };
  };
  
  /**
   * Check on "display-transformable"
   */
  afa.checkDispTrans = function (itemName, itemProperty) {
    var numOfValsForEachDispTrans = afa.AfAProperties.dispTrans.values.length;
    var tooltipText;
    
    // Get expected number of dispTrans values
    var totalNumOfVideos = $(".oer-container figure.embed.video").length;
    var total = (totalNumOfVideos + 1) * numOfValsForEachDispTrans; // includes <body> + all videos

    // find number of display-transformable values on <body>
    var dispTransValue = $(".oer-container meta[itemprop='" + itemProperty.name + "']").attr("content");
    var yes = dispTransValue.split(" ").length;

    // find number of display-transformable values on videos
    $(".oer-container figure.embed.video meta[itemprop='" + itemProperty.name + "']").each(function (index){
      var attrValue = $(this).attr("content");
      if (attrValue) {
        yes += attrValue.split(" ").length;
      } else {
          yes += 0;
      }
    });

    var level = (yes === total ? "green" : (yes === 0 ? "red" : "yellow"));

    return {
      level: level,
      tooltipText: tooltipTextMapping[itemName][level]
    };
  };
  
  /**
   * Check on "display-transformable"
   */
  afa.checkA11y = function (itemName, itemProperty) {
    var allItems = $(".oer-container meta[itemprop='" + itemProperty.name + "']");
    var accessbleItems = $("[content='true']", allItems);

    var itemsThatQualify = $(".oer-container, figure.embed.video");
    var total = itemsThatQualify.length;
    var haveProp = itemsThatQualify.find("meta[itemprop='" + itemProperty.name + "']").length;
    var yes = itemsThatQualify.find("meta[itemprop='" + itemProperty.name + "'][content='true']").length;
    var no = itemsThatQualify.find("meta[itemprop='" + itemProperty.name + "'][content='false']").length;
    var dunno = itemsThatQualify.length - haveProp;

    var level = (yes === 0 && no === 0 && total !== 0 ? "grey" : (yes === total && total === 0 ? "green" : (no === total ? "red" : "yellow")));

    return {
      level: level,
      tooltipText: tooltipTextMapping[itemName][level]
    };
  };
  
  /**
   * Check on "has-ebook"
   */
  afa.checkEbook = function (itemName, itemProperty) {
    // "has-ebook" only applies on <body>
    var total = 1;
    var yes = $(".oer-container meta[itemprop='" + itemProperty.name + "'][content='true']").length;
    var no = $(".oer-container meta[itemprop='" + itemProperty.name + "'][content='false']").length;

    var level = (yes === 0 && no === 0 && total !== 0 ? "grey" : (yes === total && total === 0 ? "green" : (no === total ? "red" : "yellow")));

    return {
      level: level,
      tooltipText: tooltipTextMapping[itemName][level]
    };
  };
  
  /**
   * Check on "unknown" type
   */
  afa.unknown = function (itemName, itemProperty) {
    return {
      level: "grey",
      tooltipText: tooltipTextMapping[itemName]["grey"]
    };
  };
  
  // End of the functions that check on AfA properties
  
  /**
   * Loop thru all AfA items to check on grade.
   */
  afa.summerizeAfA = function () {
    var tooltipText, itemTagName;
    
    fluid.each(afa.AfAProperties, function(itemProperty, itemName) {
      var result = fluid.invokeGlobalFunction(itemProperty.summaryfunc, [itemName, itemProperty]);
      // TODO: This if is only because fluid.identity returns the first argument
      if (result !== itemName) {
          afa.updateUI(itemProperty.selector, result["level"], result["tooltipText"]);
      }
    });
  };
  
  afa.addAfAToBody = function () {
    var container = $(".oer-container");
    container.attr("itemscope", "");

    // TODO: These itemprop strings should not be hard-coded
    container.prepend('<meta itemprop="is-mouse-accessible" content="true"/>');
    container.prepend('<meta itemprop="is-keyboard-accessible" content="true"/>');
    container.prepend('<meta itemprop="is-display-transformable" content="' + afa.AfAProperties.dispTrans.values.join(" ") + '"/>');
    container.prepend('<meta itemprop="has-ebook" content="false"/>');
    container.prepend('<meta itemprop="hazard" content=""/>');
  }
  
  afa.addAfAToBody();
  afa.summerizeAfA();
})();

