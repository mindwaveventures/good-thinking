console.log('NAVIGATOR');
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(function (position) {
    var location = position.coords.latitude + ',' + position.coords.longitude;
    request('get', '/location/' + location, null, function (err, res) {
      console.log(err);
      console.log(res.substring(0, 10));
    });
  });
} else {
  console.log('Navigator Geolocation not available');
}
