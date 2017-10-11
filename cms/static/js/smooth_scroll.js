var arrow = select('#browse-arrow');
var searchButton = select('#pyr-search');

function scrollToElement (e, elementId) {
  e.preventDefault();
  var element = select(elementId);
  var targetPos = element.offsetTop - element.offsetHeight;

  window.scrollTo({
    top: targetPos,
    left: 0,
    behavior: 'smooth'
  });
}

arrow.addEventListener('click', function (e) {
  scrollToElement(e, '#topics');
});

searchButton.addEventListener('click', function (e) {
  scrollToElement(e, '#results');
});
