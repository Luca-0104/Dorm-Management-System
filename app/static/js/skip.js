// JavaScript Document
$('#student').click(function () {
	alert('/login');
	location.href = '/login?identification=student'
});

$('#dormintoryAdmin').click(function () {
	alert('/login');
	location.href = '/login?identification=dormitoryAdmin'
});

$('#systemAdmin').click(function () {
	alert('/login');
	location.href = '/login?identification=systemAdmin'
});
