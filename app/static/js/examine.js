$('#registerID').blur(function () {
    let phone = $(this).val();
    let span_ele = $(this).next('span');
    if(phone.length===7) {
        span_ele.text('')
        $.get('checkphone', {phone: phone}, function (data) {
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