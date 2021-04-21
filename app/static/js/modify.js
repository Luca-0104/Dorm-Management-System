// JavaScript Document
$('#sendMessage').click(function(){
	let ID = $("input[name='stu_ID']").val();
	let phone = $("input[name='phone']").val();
	let email = $("input[name='email']").val();
	let room = $("input[name='room']").val();
	let name = $("input[name='name']").val();
	console.log(ID,phone,email,room,name);	
});