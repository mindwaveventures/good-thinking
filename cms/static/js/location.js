function handleGeolocationMessage () {
  if (document.cookie.indexOf('ldmw_shown_location_message') > -1) {
    return;
  }
  var geolocationMessage = document.createElement('div');
  geolocationMessage.className = 'lm-bg-dark-blue lm-white w-100 tc z-4 absolute top-0 f5';
  var fontSize = parseFloat(window.getComputedStyle(select('body'), null).getPropertyValue('font-size'));
  geolocationMessage.id = 'geolocation_message_id';
  var betaBannerHeight = (select('#beta-banner') || {}).clientHeight || 0;
  geolocationMessage.style.marginTop = betaBannerHeight + 'px';
  geolocationMessage.style.height = betaBannerHeight + 'px';
  geolocationMessage.style.paddingTop = (betaBannerHeight - fontSize) / 2 + 'px';
  geolocationText = document.createTextNode('We are using your location to make your search results more tailored to you');
  geolocationMessage.appendChild(geolocationText);
  select('body').appendChild(geolocationMessage);
  function removeGeolocation_message() {
    select('#geolocation_message_id').style.WebkitTransition = 'opacity 1s';
    select('#geolocation_message_id').style.MozTransition = 'opacity 1s';
    select('#geolocation_message_id').style.opacity = '0';
    select('#geolocation_message_id').style.zIndex = '-1';
    document.cookie = 'ldmw_shown_location_message=1'; /* only lasts for browser session */
  }
  window.setTimeout(removeGeolocation_message, 5000);
}

if (navigator.geolocation) {
  if (document.cookie.indexOf('ldmw_location_latlong') > -1) {
    handleGeolocationMessage();
  } else {
    navigator.geolocation.getCurrentPosition(function (position) {
      var location = position.coords.latitude + ',' + position.coords.longitude;
      document.cookie = 'ldmw_location_latlong=' + location;
      window.location.reload();
    });
  }
} else {
  console.log('Navigator Geolocation not available');
}
