$(document).ready(function() {
    progressStr = $(".progress-span").attr("name").split(",");
    lessonsCompleted = Number(progressStr[0].substring(1));
    lessonProgress = Number(progressStr[1].substring(progressStr[1].length));
    currentLesson = lessons[lessonsCompleted];
    currentActivity = currentLesson.activities[lessonProgress];

    newHTML = htmlForActivity(currentActivity, lessonProgress, currentLesson, lessonsCompleted);
    $("#card-holder").append(newHTML);
    percent = Number(lessonProgress * 100 / currentLesson.activities.length);
    percentStr = `${ percent }%`;
    $("#progress").css("width", percentStr);
    $("#progress").text(percentStr);
});