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
            console.log(data);
        },
        error : function(xhr,errmsg,err) {
            $('#results').html(+errmsg); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
});