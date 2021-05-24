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

$('#search3').click(function(){
	let content = $("input[name='search_da']").val();
	var tag = document.getElementById("inputGroupSelect03").value;
	location.href="/dormAdmin/search_gue?content="+content+"&tag="+tag;
});

