var bodyText = select('.see_more_body .rich-text');

if (bodyText) {
  var bodyChildren = bodyText.children;

  var display = getHTMLToShow(bodyChildren);

  if (display.hideElements.length) {
    var seeMore = document.createElement('a');
    var seeLess = document.createElement('a');

    seeMore.className = "pointer"
    seeMore.innerText = "See more"
    seeLess.className = "pointer"
    seeLess.innerText = "See less"

    bodyText.innerHTML = "";

    displayBody(display.showElements);
    bodyText.appendChild(seeMore);

    seeMore.addEventListener('click', function(e) {
      bodyText.innerHTML = "";
      displayBody(display.showElements.concat(display.hideElements, seeLess))
    });

    seeLess.addEventListener('click', function(e) {
      bodyText.innerHTML = "";
      displayBody(display.showElements.concat(seeMore))
    });
  }
}

function getHTMLToShow(elements) {
  var showElements = [];
  var hideElements = [];
  var display = true;

  for (var i = 0; i < elements.length; i++) {
    if (display) {
      showElements.push(elements[i])
    } else {
      hideElements.push(elements[i])
    }

    if (elements[i].nodeName === "P" && elements[i].innerText.length > 0) {
      display = false;
    }
  };

  return {
    showElements: showElements,
    hideElements: hideElements
  }
}

function displayBody(elements) {
  for (var i = 0; i < elements.length; i++) {
    bodyText.appendChild(elements[i]);
  }
}
