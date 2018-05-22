$('#id_program').change(function() {
    var program = $(this).val();
    var courses = $('#id_course');

    $.ajax({
        url: '/ajax/filter_course/',
        type: 'get',
        data: {
            'program': program
        },
        dataType: 'json',
        success: function(data) {
            $(courses).children('option').remove();
            $(data).each(function(i, el) {
                $(courses).append('<option value="'+ el.pk +'">' + el.name + '</option>');
            })
        },
        error : function(xhr,errmsg,err) {
            $('#results').html(+errmsg);
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});