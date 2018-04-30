
function GetResults(slug) {
  var array = [];
  var url = "";
  $("input:checkbox[name=1]:checked").each(function(){
    array.push({query:'q1',value:$(this).val()});
  });
  $("input:checkbox[name=2]:checked").each(function(){
    array.push({query:'q2',value:$(this).val()});
  });
  $("input:checkbox[name=3]:checked").each(function(){
    array.push({query:'q3',value:$(this).val()});
  });
  array.forEach(function(e){
     url += e.query+ "=" + e.value + "&";
  });
  url = url.trim("&");
  window.location.href='/results/?'+url+'slug='+slug;
 }
