$('#id_exercise').select2()
$('#id_exercise_name').select2()
if (document.title==='Training Log Create Training Plan'|| document.title==='Training Log Training Plan'){
    $('#id_training_plan_name').select2()
}
// Date.prototype.getWeek = function () { return $.datepicker.iso8601Week(this); }
if (document.title==='Training Log Workout List'){
    // const date = document.getElementById('id_date')
    // date.addEventListener('change', function (){
    //     $('#id_date').value.datepicker.iso8601Week.value
    //     console.log(date.value)
    // })
    // console.log(date.value)

//     $('#id_date').datepicker({
//     defaultDate: new Date()
// });
    // $('#id_date').datepicker("setDate" , new Date());

    $('#id_date').datepicker( {
        changeMonth: true,
        changeYear: true,
        yearRange: '2022:2122',
        onSelect: function (date, inst) {
            const value = $('#id_date').val()
            const firstDate = moment(value).day(0).format('YYYY-MM-DD');
            const lastDate =  moment(value).day(6).format('YYYY-MM-DD');
            const range = $('#id_date').val(firstDate + '   -   ' + lastDate);
        const week = $('#weekNumber').val($.datepicker.iso8601Week(new Date(date)))
        location.href = week.val();
        $('#week1Number').val(date);
    }

});
    // console.log(location.href)
    // $('#id_date').datepicker().datepicker('setDate', 'now')
    const firstDay =  $('#id_date').datepicker('option', 'firstDay');
    $('#id_date').datepicker('option', 'firstDay', 1);



    // $('#id_date').datepicker({
    // onSelect: function (date, inst) {
    //     $('#week1Number').val($.datepicker.getFullYear());
    // }
    // });
}