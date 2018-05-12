
function GetQueryResults(slug) {

  var query_result = [];
  var url = "";

  $("input:checkbox[name=1]:checked").each(function(){
    query_result.push({query:'q1',value:$(this).val()});
  });
  $("input:checkbox[name=2]:checked").each(function(){
    query_result.push({query:'q2',value:$(this).val()});
  });
  $("input:checkbox[name=3]:checked").each(function(){
    query_result.push({query:'q3',value:$(this).val()});
  });
  query_result.forEach(function(e){
     url += e.query+ "=" + e.value + "&";
  });
  url = url.trim("&");
  window.location.href='/results/'+slug+'/'+'?'+url;

 }

function GetCollectionResults(collection_slug) {
 window.location.href='/collections/'+collection_slug;
}

function RemoveResource(resource){
  $('.'+ resource).remove();
  document.getElementById("resource_count").innerHTML = stress_result_swiper();
}

function ScrollUp(resource){
  $('.'+ resource).scrollTop(300);
}
