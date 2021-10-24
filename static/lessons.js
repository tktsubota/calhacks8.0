$(document).ready(function() {
    progressStr = $(".progress-span").attr("name").split(",");
    lessonsCompleted = Number(progressStr[0].substring(1));
    lessonProgress = Number(progressStr[1].substring(progressStr[1].length));

    for (var i = 0; i < lessons.length; i++) {
        lesson = lessons[i]
        active = false;
        if (i < lessonsCompleted) {
            fraction = 1
        } else if (i > lessonsCompleted) {
            fraction = 0
        } else {
            fraction = lessonProgress / lesson.activities.length
            active = true
        }
        newHTML = htmlForLesson(lesson, i, fraction, active);
        $("#lesson-list").append(newHTML);
    }
});