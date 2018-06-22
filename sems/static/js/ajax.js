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
                    $(courses).append('<option value="'+ el.pk +'"' + (el.obligative ? "selected" : "") + '>' + el.name + '</option>');
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


$("#update_teacher_btn").click(function() {
    var val1 = $("#user_1").val();
    var c = $("#course").val();

    console.log(c + ": " + val1);

    $.ajax({
        url: '/ajax/update/teacher/',
        type: 'get',
        data: {
            'c_pk': c,
            'pk_t1': val1,
        },
        dataType: 'json',
        success: function(data) {
            $("#msg").addClass('alert alert-success');
            $("#msg").text('Teacher Updated');
        },
        error : function(xhr,errmsg,err) {
            $('#results').html(+errmsg);
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });

});


$("#filterProvimet").change(function() {

    var content = $("#provimetTable");

    $.ajax({
        url: '/ajax/filter/provimet/',
        type: 'get',
        data: { 'afati': $("#filterProvimet").val(), },
        dataType: 'json',
        success: function(data) {
            content.html(data);
            console.log(data);
        },
        error : function(xhr,errmsg,err) {
            $('#results').html(+errmsg);
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });

});