$(document).ready(function() {
    current = this.location.pathname
    if (current == "/") {
        if (!$("#nav-home").hasClass("active")) {
            $("#nav-home").addClass("active")
        }
    } else if (current == "/lessons") {
        if (!$("#nav-lessons").hasClass("active")) {
            $("#nav-lessons").addClass("active")
        }
    } else if (current == "/simulator") {
        if (!$("#nav-simulator").hasClass("active")) {
            $("#nav-simulator").addClass("active")
        }
    }

    // $(".lesson-circle").mousedown(function() {
    //     $(this).css('box-shadow', '0px 0px 0px #000');
    // })
    // $(".lesson-circle").mouseup(function() {
    //     $(this).css('box-shadow', '5px 5px 5px lightgray');
    // })
});