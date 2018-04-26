
$(document).ready(function(){
  $('#MyButton').click(function(){
    console.log("checkbox");
  var obj = {q1:[],q2:[],q3:[]};
  $("input:checkbox[name=1]:checked").each(function(){
    obj.q1.push($(this).val());
  });
  $("input:checkbox[name=2]:checked").each(function(){
    obj.q2.push($(this).val());
  });
  $("input:checkbox[name=3]:checked").each(function(){
    obj.q3.push($(this).val());
  });
  console.log(obj);
  });
});
