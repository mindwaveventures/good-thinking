var qInfoButton = select('#toggle-q-info');
var qInfo = select('#q-info');
var aInfoButton = select('#toggle-a-info')

function addInfoListener (element) {
  element.addEventListener('click', function (e) {
    e.preventDefault();
    qInfo.classList.toggle("dn")
  });
}

if (!!qInfoButton && !!qInfo) {
  addInfoListener(qInfoButton);
}

if (!!aInfoButton && !!qInfo) {
  addInfoListener(aInfoButton);
}
