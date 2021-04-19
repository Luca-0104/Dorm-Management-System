// JavaScript Document
$('#search1').click(function(){
	let content = $("input[name='search']").val();
	var tag = document.getElementById("inputGroupSelect01").value;
	location.href="/dormAdmin/search_stu?content="+content+"&tag="+tag;
});

$('#search2').click(function(){
	let content = $("input[name='search_gue']").val();
	var tag = document.getElementById("inputGroupSelect02").value;
	location.href="/dormAdmin/search_gue?content="+content+"&tag="+tag;
});

