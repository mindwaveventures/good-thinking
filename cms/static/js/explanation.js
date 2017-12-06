var qInfoButton = select('#toggle-q-info');
var qInfo = select('#q-info');

function addInfoListener (element, qInfo) {
  element.addEventListener('click', function (e) {
    var qInfo_asset_id = qInfo.getAttribute('data-asset-id');
    var qInfo_node_type_id = qInfo.getAttribute('data-node-type-id');

    var iButton = e.target;
    var iButton_node_type_id;

    if (!!iButton.name) {
      switch (iButton.name) {
        case 'a_info':
          iButton_node_type_id = '64';
          break;
        case 'q_info':
          iButton_node_type_id = '32';
          break;
      }
    }

    if (!!qInfo && qInfo_asset_id == iButton.value && qInfo_node_type_id == iButton_node_type_id) {
      // qInfo panel is showing, and it is for node type (question/answer) and for the same asset, so go ahead and hide it
      e.preventDefault();
      qInfo.classList.toggle("dn")
    }

    // otherwise, do nothing.  Default bahviour will be to load the information box for the button selected
  });
}

if (!!qInfoButton && !!qInfo) {
  addInfoListener(qInfoButton, qInfo);
}

if (!!qInfo) {
  selectAll(".toggle-a-info").forEach(function(aInfoButton) {
    addInfoListener(aInfoButton, qInfo);
  });
}
