$('#id_exercise').select2()
$('#id_exercise_name').select2()
if (document.title === 'Training Log Create Training Plan' || document.title === 'Training Log Training Plan') {
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
            location.href = change.val();
        })
    })


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

}