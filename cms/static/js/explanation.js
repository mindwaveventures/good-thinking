var qInfoButton = select('#toggle-q-info');
var qInfo = select('#q-info');
if (!!qInfoButton && !!qInfo) {
  qInfoButton.addEventListener('click', function (e) {
    e.preventDefault();
    qInfo.classList.toggle("dn")
  });
}
