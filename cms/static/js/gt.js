
$(document).ready(function(){
  var obj = {query1:[],query2:[],query3:[]};
  $('#MyButton').click(function(){
  $("input:checkbox[name=1]:checked").each(function(){
    obj.query1.push($(this).val());
  });
  $("input:checkbox[name=2]:checked").each(function(){
    obj.query2.push($(this).val());
  });
  $("input:checkbox[name=3]:checked").each(function(){
    obj.query3.push($(this).val());
  });
    console.log(obj);
  });
});
