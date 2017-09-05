if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(function (position) {
    var location = position.coords.latitude + ',' + position.coords.longitude;
    request('get', '/location/' + location, null, function (err, res) {
      if (err) {
        console.log('Problem getting geolocation');
        return;
      }
      console.log('Adding geolocation to user session');
    });
  });
} else {
  console.log('Navigator Geolocation not available');
}
