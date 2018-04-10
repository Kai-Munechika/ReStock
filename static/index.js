$(document).ready(function () {
    // all custom jQuery will go here
    $('.dropdown-trigger').dropdown();
    $('select').formSelect();
    var form = document.getElementById("user_search");
    document.getElementById("pressed_search").addEventListener("click", function () {
        form.submit();
    });
});





