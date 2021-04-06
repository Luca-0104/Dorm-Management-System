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

// $('#EmailLogin').click(function () {
// // 	alert("hello")
// // 	location.href = 'auth/login?f=3'
// // });
// //
// // $('#UserLogin').click(function () {
// // 	alert("hello")
// // 	location.href = 'auth/login?f=2'
// // });
// //
// // $('#PhoneLogin').click(function () {
// // 	alert("hello")
// // 	location.href = 'auth/login?f=1'
// // });

function skipPhone(role){
	location.href='login?identification='+role+"&f=1"
}

function skipEmail(role) {
	location.href='login?identification='+role+"&f=2"
}

function skipUser(role) {
	location.href='login?identification='+role
}