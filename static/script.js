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
});