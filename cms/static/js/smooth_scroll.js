var arrow = select('#browse-arrow');

arrow.addEventListener('click', function (e) {
  e.preventDefault();
  var topics = select('#topics');
  var targetPos = topics.offsetTop - topics.offsetHeight;

  window.scrollTo({
    top: targetPos,
    left: 0,
    behavior: 'smooth'
  });
});
