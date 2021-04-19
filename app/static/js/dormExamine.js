$('#stu_id').blur(function () {
    let id = $(this).val();
    let span_ele = $(this).next('span');
    console.log(id);
    if(id.length===8) {
        span_ele.text('');
        $.get('dormAdmin/dormCheckID', {id: id}, function (data) {
            // console.log(data)
            if(data.code !== 200){
                span_ele.css({"color": "#ff0011","font-size":"12px"});
                span_ele.text(data.msg);
            }
        })
    }else {
        span_ele.css({"color":"#ff0011","font-size":"12px"});
        span_ele.text('The unacceptable ID format');
    }
});

$('#gue_stu_id').blur(function () {
    let id = $(this).val();
    let span_ele = $(this).next('span');
    console.log(id);
    if(id.length===8) {
        span_ele.text('');
        $.get('dormAdmin/dormCheckID', {id: id}, function (data) {
            // console.log(data)
            if(data.code !== 200){
                span_ele.css({"color": "#ff0011","font-size":"12px"});
                span_ele.text(data.msg);
            }
        })
    }else {
        span_ele.css({"color":"#ff0011","font-size":"12px"});
        span_ele.text('The unacceptable ID format');
    }
});

$('#email').blur(function () {
    let email = $(this).val();
    let span_ele = $(this).next('span');
        span_ele.text('');
        $.get('dormAdmin/dormCheckEmail', {email: email}, function (data) {
            // console.log(data)
            if(data.code !== 200){
                span_ele.css({"color": "#ff0011","font-size":"12px"});
                span_ele.text(data.msg);
            }
        })
});

$('#phone').blur(function () {
    let phone = $(this).val();
    let span_ele = $(this).next('span');
    if(phone.length===11) {
        span_ele.text('');
        $.get('dormAdmin/dormCheckPhone', {phone: phone}, function (data) {
            // console.log(data)
            if(data.code !== 200){
                span_ele.css({"color": "#ff0011","font-size":"12px"});
                span_ele.text(data.msg);
            }
        })
    }else {
        span_ele.css({"color":"#ff0011","font-size":"12px"});
        span_ele.text('The unacceptable ID format');
    }
});