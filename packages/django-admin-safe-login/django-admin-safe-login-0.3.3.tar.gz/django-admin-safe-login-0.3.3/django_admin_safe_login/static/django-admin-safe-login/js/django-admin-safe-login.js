;!(function(){
    $(document).ready(function(){
        $('.captcha').click(function(){
            $.getJSON("/captcha/refresh/", function (result) {
                $('.captcha').attr('src', result['image_url']);
                $('#id_captcha_0').val(result['key'])
            });
        });
    });
})(jQuery);
