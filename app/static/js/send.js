$('#btnCheck').click(function () {
    let phone = $('#inputPhone').val();
    if(!phone && phone.length===11 ){
        $.get('auth/sendMsg',{phone:phone},function (data) {
        });
    }else{
        alert("You must enter the correct phone number")
    }
});