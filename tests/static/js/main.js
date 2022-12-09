$(document).ready(function(){
    $('form').on('input', function (){
        $('#next-question').prop('disabled',  $('input').filter(':checked').length < 1)
    })
});