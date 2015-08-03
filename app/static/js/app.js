$("#toggle-nav").click(function(){
    $(".container").toggleClass("open");
})

$("#reveal-form").click(function(){
    $(".save-the-date").toggleClass("reveal-form");
    return false;
})