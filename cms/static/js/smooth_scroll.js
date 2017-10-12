var arrow = select('#browse-arrow');

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
