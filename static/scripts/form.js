$('#id_exercise').select2()
$('#id_exercise_name').select2()
if (document.title === 'Training Log Create Training Plan' || document.title === 'Training Log Training Plan' || document.title === 'Training Log Workout') {
    $('#id_training_plan_name').select2()
}
if (document.title === 'Training Log Workout List') {
    $('#id_date').datepicker({
        weekStart: 1,
        maxViewMode: 'years',
        defaultViewDate: 'today'
    }).on('changeDate', function (ev) {
        $('#id_date').change(function () {
            const change = $('#id_date').val($.datepicker.iso8601Week(new Date($('#id_date').val())))
            const url = location.href.split('/')
            url[6] = ev.date.getFullYear().toString()
            url[7] = change.val()
            location.href = url.join('/')
        })
    })
}

if (document.title === 'Training Log Create Training Plan' || document.title === 'Training Log Workout') {
    $("#id_training_plan_name").change(function () {
        const url = $("#Trainingplanform").attr("training-url");  // get the url of the `load_cities` view
        const trainingId = $(this).val();
        // get the selected country ID from the HTML input
        if (trainingId.length > 0) {


            $.ajax({                       // initialize an AJAX request
                url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
                data: {
                    'training_plan_name': trainingId       // add the country id to the GET parameters
                },
                success: function (data) {
                    $("#id_training").html(data);
                },
            });
        } else {
            $('#id_training').prop("selectedIndex", -1)
            $('#id_training').empty()
        }
    });
}

if (document.title === 'Training Log Workout') {
    $("#id_training").change(function () {
        const url1 = $("#Trainingform").attr("training1-url");  // get the url of the `load_cities` view
        const training1Id = $(this).val();
        console.log(training1Id)
        // get the selected country ID from the HTML input
        if (training1Id.length > 0) {


            $.ajax({                       // initialize an AJAX request
                url: url1,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
                data: {
                    'training_id': training1Id       // add the country id to the GET parameters
                },
                success: function (data) {
                    $("#id_exercise").html(data);
                    // $("#test").html(data);
                },
            });
        } else {
            $('#id_exercise').prop("selectedIndex", -1)
            $('#id_exercise').empty()
        }
    });
}


//     $('#id_date').datepicker( {
//         changeMonth: true,
//         changeYear: true,
//         yearRange: '2022:2122',
//         onSelect: function (date, inst) {
//             const value = $('#id_date').val()
//             const firstDate = moment(value).day(0).format('YYYY-MM-DD');
//             const lastDate =  moment(value).day(6).format('YYYY-MM-DD');
//             const range = $('#id_date').val(firstDate + '   -   ' + lastDate);
//         const week = $('#weekNumber').val($.datepicker.iso8601Week(new Date(date)))
//         location.href = week.val();
//         $('#week1Number').val(date);
//     }
//
// });
// $('#id_date').datepicker().datepicker('setDate', 'now')
// const firstDay =  $('#id_date').datepicker('option', 'firstDay');
// $('#id_date').datepicker('option', 'firstDay', 1);

