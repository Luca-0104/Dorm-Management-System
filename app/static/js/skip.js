// JavaScript Document
$('#student').click(function () {
	location.href = 'auth/login?identification=student'
});

$('#dormintoryAdmin').click(function () {
	location.href = 'auth/login?identification=dormitoryAdmin'
});

$('#systemAdmin').click(function () {
	location.href = 'auth/login?identification=systemAdmin'
});
