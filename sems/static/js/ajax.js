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
            if ($('#id_program').attr('data-type') != 'program-listener') {
                $(courses).children('option').remove();
                $(data).each(function(i, el) {
                    $(courses).append('<option value="'+ el.pk +'">' + el.name + '</option>');
                });
            } else {
                $(courses).children('li').remove();
                $(data).each(function(i, el) {
                    $(courses).append('<li><label for="id_course_' + (i+1) + '">' +
                                    '<input type="checkbox" name="course" value="' + el.pk + '" id="id_course_' + (i+1) + '"> ' +
                                     el.name +
                                 '</label></li>');
                });
            }
        },
        error : function(xhr,errmsg,err) {
            $('#results').html(+errmsg);
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});