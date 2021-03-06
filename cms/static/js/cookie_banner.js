var our_cookie = 'ldmw_accepted_cookie_policy=1';
function toggleClasses(element, classes) {
  classes.forEach(function(c) {
    element.classList.toggle(c);
  });
}

// Aliases for querySelector functions
// Uses document.querySelector if no parent is passed
function select(query, parent) {
  return parent ? parent.querySelector(query) : document.querySelector(query);
}

function show_cookie_bar () {
  // if we have accepted the cookie policy
  if (document.cookie.indexOf(our_cookie) > -1) {
    // if the banner is showing
    if (select('#cookie_accept_bar').className.indexOf('hide_cookie') === -1) {
      // stop showing the banner
      toggleClasses(select('#cookie_accept_bar'), ['hide_cookie']);
      toggleClasses(select('#blank_div_id'), ['hide_cookie']);
    }
    return;
  }

  toggleClasses(select('#cookie_accept_bar'), ['hide_cookie']);
  add_blank_div_to_not_cover_content();
}

function accept_cookie_listener() {
  select('#cookie_accept_bar > button')
    .addEventListener('click', function (e) {
      e.preventDefault();
      var d = new Date();
      var one_day = 24 * 60 * 60 * 1000;
      d.setTime(d.getTime() + one_day);
      var expires = ';expires=' + d.toUTCString();
      document.cookie = our_cookie + expires + ";path=/";
      show_cookie_bar();
    });
}

function add_blank_div_to_not_cover_content() {
  // Add a blank div here to ensure that no content is covered by the cookie banner
  var blank_div = document.createElement('div');
  blank_div.id = 'blank_div_id';
  blank_div.style.height = document.querySelector('#cookie_accept_bar').clientHeight + 'px';
  select('body').appendChild(blank_div);
}

document.addEventListener('DOMContentLoaded', function () {
  show_cookie_bar();
  accept_cookie_listener();
});
