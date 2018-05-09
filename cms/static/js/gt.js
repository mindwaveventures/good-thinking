
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
  window.location.href='/results/'+slug+'/'+'?'+url+'slug='+slug;

 }


 function GetCollectionResults(classname) {
   var collection_result = [];
   var url = "";

   $('.'+ classname).each(function(){
       collection_result.push({query:'page',value:$(this).val()});
   });

   collection_result.forEach(function(e){
      url += e.value + ",";
   });

   url = url.trim(",");
   window.location.href='/results/collections?page='+url;
  }
