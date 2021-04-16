// JavaScript Document
$('#search1').click(function(){
	let content = $("input[name='search']").val();
	var obj = document.getElementById("inputGroupSelect01").value;
	location.href="https://www.baidu.com";
	console.log(content,obj);
});

$('#delete').click(function(){
	location.href="https://www.baidu.com";
});

