(function () {
  var hamburger = select('#hamburger_id');
  var closeHamburger = select('#hamburger_close');
  var hamburger_content = select('#hamburger_content_id');
  var beta_banner = select('#beta-banner');

  function toggleHamburger(e) {
    resize();
    hamburger = select('#hamburger_id');
    hamburger_content = select('#hamburger_content_id');
    var hamburgerIsOpen = hamburger.className.indexOf('active') > -1;

    if (hamburgerIsOpen) {
      // hiding hamburger content
      hamburger.classList.remove('active');
      hamburger_content.classList.remove('show_hamburger');
      select('body').classList.remove('stop-scrolling');
      select('html').classList.remove('stop-scrolling');
    } else {
      // showing hamburger content
      hamburger.classList.add('active');
      hamburger_content.classList.add('show_hamburger');
      select('body').classList.add('stop-scrolling');
      select('html').classList.add('stop-scrolling');
    }
  }

  function positionHamburger() {
    beta_banner = select('#beta-banner');
    select('#landing_page_hamburger').style.top = ((beta_banner || {}).clientHeight || 0) + "px";
  }

  function resize  () {
    if (hamburger) {
      positionHamburger();
    }
  }

  if (hamburger) {
    hamburger.addEventListener('click', toggleHamburger);
  }

  if (closeHamburger) {
    closeHamburger.addEventListener('click', toggleHamburger);
  }

  window.addEventListener('resize', resize);
  resize();
})();
