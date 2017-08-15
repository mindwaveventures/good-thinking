(function () {
  var hamburger = select('#hamburger_id');
  var hamburger_content = select('#hamburger_content_id');
  var beta_banner = select('#beta-banner');

  function toggleHamburger(e) {
    resize();
    hamburger = select('#hamburger_id');
    hamburger_content = select('#hamburger_content_id');
    var hamburgerIsOpen = hamburger.className.indexOf('is-active') > -1;

    if (hamburgerIsOpen) {
      // hiding hamburger content
      hamburger.classList.remove('is-active');
      hamburger_content.classList.remove('show_hamburger');
      select('body').classList.remove('stop-scrolling');
    } else {
      // showing hamburger content
      hamburger.classList.add('is-active');
      hamburger_content.classList.add('show_hamburger');
      select('body').classList.add('stop-scrolling');
    }
  }

  function sizeHamburgerContent() {
    hamburger = select('#hamburger_id');
    hamburger_content = select('#hamburger_content_id');
    beta_banner = select('#beta-banner');
    var topContentHeight = hamburger.clientHeight + ((beta_banner || {}).clientHeight || 0);

    hamburger_content.style.height = (window.innerHeight + window.scrollY - topContentHeight) + "px";
    hamburger_content.style.marginTop = topContentHeight + "px";
  }

  function positionHamburger() {
    beta_banner = select('#beta-banner');
    select('#landing_page_hamburger').style.top = ((beta_banner || {}).clientHeight || 0) + "px";
  }

  function resize  () {
    sizeHamburgerContent();
    positionHamburger();
  }

  hamburger.addEventListener('click', toggleHamburger);

  window.addEventListener('resize', resize);
  resize();
})();
