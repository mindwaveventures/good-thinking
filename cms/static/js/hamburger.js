(function () {
  function toggle(e) {
    if (hamburger.className.indexOf('is-active') > -1) {
      hamburger.classList.remove('is-active');
      hamburger_content.classList.remove('show_hamburger');
    } else {
      hamburger.classList.add('is-active');
      hamburger_content.classList.add('show_hamburger');
    }
  }
  var hamburger = document.querySelector('#hamburger_id');
  var hamburger_content = document.querySelector('#hamburger_content_id');
  var beta_banner = document.querySelector('#beta-banner');
  hamburger.addEventListener('click', toggle);
  (function sizeHamburgerContent() {
    var topContent = hamburger.clientHeight + beta_banner.clientHeight - 10;
    hamburger_content.style.height = (window.innerHeight - topContent) + "px";
    hamburger_content.style.marginTop = topContent + "px";
  })();
})();
