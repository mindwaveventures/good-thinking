var qInfoButton = select('#toggle-q-info');
var qInfo = select('#q-info');

function addInfoListener (element) {
  element.addEventListener('click', function (e) {
    var node_type_id;

    if (!!e.name) {
      switch (e.name) {
        case 'a_info':
          node_type_id = '64';
          break;
        case 'q_info':
          node_type_id = '32';
          break;
      }
    }

    if (!!qInfo && qInfo.getAttribute('data-asset-id') == e.value && qInfo.getAttribute('data-node-type-id') == node_type_id) {
      // qInfo panel is showing, and it is for node type (question/answer) and for the same asset, so go ahead and hide it
      e.preventDefault();
      qInfo.classList.toggle("dn")
    }

    // otherwise, do nothing.  Default bahviour will be to load the information box for the button selected
  });
}

if (!!qInfoButton && !!qInfo) {
  addInfoListener(qInfoButton);
}

if (!!qInfo) {
  selectAll(".toggle-a-info").forEach(function(aInfoButton) {
    addInfoListener(aInfoButton);
  });
}
