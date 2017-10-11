var bodyText = select('.see_more_body .rich-text');

if (bodyText) {
  var bodyChildren = bodyText.children;

  var display = getHTMLToShow(bodyChildren);
  var seeMore = document.createElement('a');

  seeMore.className = "pointer"
  seeMore.innerText = "See more"

  bodyText.innerHTML = "";

  displayBody(display.showElements);
  bodyText.appendChild(seeMore);

  seeMore.addEventListener('click', function(e) {
    seeMore.style.display = "none";
    displayBody(display.hideElements)
  });
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
