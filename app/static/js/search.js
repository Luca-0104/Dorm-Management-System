// JavaScript Document
$('#search1').click(function(){
	let content = $("input[name='search']").val();
	var tag = document.getElementById("inputGroupSelect01").value;
	location.href="/dormAdmin/search_stu?content="+content+"&tag="+tag;
	console.log(content,tag);
});

$('#delete').click(function(){
	location.href="/dormAdmin/search_stu";
});

