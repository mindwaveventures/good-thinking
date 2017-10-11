function handleViewProsCons (e, el) {
  toggleClasses(select('#pros_cons' + getResourceId(el)), ['dn']);
  changeInnerHtml(el);
}

function changeInnerHtml (el) {
  if (el.innerHTML === 'View pros and cons') {
    el.innerHTML = 'Hide pros and cons';
  } else {
    el.innerHTML = 'View pros and cons';
  }
}

function proConListeners() {
  selectAll('.view_pcs').forEach(function (el) {
    el.addEventListener('click', function (e) {
      handleViewProsCons(e, el);
    });
  });
}

// shows button for toggle pros/cons. Needs to grab parentNode as this is what is dn
function reverseButtonVisibility (el) {
  removeClasses(el.parentNode, ['dn']);
  addClasses(el.parentNode, ['db']);
}

// hides the list of pros and cons
function reverseListVisibility (el) {
  removeClasses(el, ['dt']);
  addClasses(el, ['dn']);
}

// checks if pros and cons are on the page that's being view, and if it's mobile
function mobileProsAndCons () {
  console.log('MOBILE PROS AND CONS');
  if (selectAll('.pros_cons').length > 0 && isMobile()) {
    selectAll('.pros_cons').forEach(function (el) {
      reverseListVisibility(el);
    });
    selectAll('.view_pcs').forEach(function (el) {
      reverseButtonVisibility(el);
    });
    proConListeners();
  }
}

mobileProsAndCons();
