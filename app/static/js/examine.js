$('#registerID').blur(function () {
    let id = $(this).val();
    let span_ele = $(this).next('span');
    if(id.length===8) {
        span_ele.text('')
        $.get('checkID', {id: id}, function (data) {
            // console.log(data)
            if(data.code !== 200){
                span_ele.css({"color": "#ff0011","font-size":"12px"})
                span_ele.text(data.msg);
            }
        })
    }else {
        span_ele.css({"color":"#ff0011","font-size":"12px"});
        span_ele.text('The unacceptable ID format');
    }
});

$('#registerEmail').blur(function () {
    let email = $(this).val();
    let span_ele = $(this).next('span');
        span_ele.text('')
        $.get('checkEmail', {email: email}, function (data) {
            // console.log(data)
            if(data.code !== 200){
                span_ele.css({"color": "#ff0011","font-size":"12px"})
                span_ele.text(data.msg);
            }
        })
});

$('#registerPhone').blur(function () {
    let phone = $(this).val();
    let span_ele = $(this).next('span');
    if(phone.length===11) {
        span_ele.text('')
        $.get('checkPhone', {phone: phone}, function (data) {
            // console.log(data)
            if(data.code !== 200){
                span_ele.css({"color": "#ff0011","font-size":"12px"})
                span_ele.text(data.msg);
            }
        })
    }else {
        span_ele.css({"color":"#ff0011","font-size":"12px"});
        span_ele.text('The unacceptable ID format');
    }
});

$('#registerCPassword').blur(function () {
    let pass = $('#registerPassword').val();
    let cpass = $(this).val()
    let span_ele = $(this).next('span');
    if(pass !== cpass) {
        span_ele.css({"color":"#ff0011","font-size":"12px"});
        span_ele.text('The password are not matched!');
    }
});

$('#signUp').click(function () {
    let pass = $('#registerPassword').val();
    let cpass = $('#registerCPassword').val()
    if(pass !== cpass) {
        alert('The password are not matched!')
    }else {
        alert("register successfully")
    }
})