// JavaScript Document
$('#student').click(function () {
	location.href = 'auth/login?identification=1'
});

$('#dormintoryAdmin').click(function () {
	location.href = 'auth/login?identification=2'
});

$('#systemAdmin').click(function () {
	location.href = 'auth/login?identification=3'
});
