class Activity {
    text;
    constructor(text) {
        this.text = text;
    }
}

class MultipleChoiceActivity extends Activity {
    question;
    options;
    correctIndex;
    constructor(text, question, options, correctIndex) {
        super(text);
        this.question = question;
        this.options = options;
        this.correctIndex = correctIndex;
    }
}

class GraphActivity extends Activity {
    correctSlope;
    constructor(text, correctSlope) {
        super(text);
        this.correctSlope = correctSlope;
    }
}

class Lesson {
    name;
    icon;
    activities;
    constructor(name, icon, activities) {
        this.name = name;
        this.icon = icon;
        this.activities = activities;
    }
}

// Hardcoded data begin
lessons = []

// Lesson 1
activities1 = []
activities1.push(new Activity("In this lesson you will learn about investing and saving."));
activities1.push(new MultipleChoiceActivity(
    "Financial investing is purchasing portions of companies (stocks), a collection of managed stocks (mutual funds) and cryptocurrency.",
    "What is an example of an investment?",
    ["Putting money in a bank account", "Buying food", "Finding a job", "Buying a stock of Apple"],
    3));
activities1.push(new GraphActivity(
    "Holding investments for long periods of time(long term investing) is generally the safest way to make money through financial investments.",
    "Based on the average long term investment, which direction should your money go over time?",
    1));
activities1.push(new GraphActivity(
    "Your money decreases in value as the government prints more money each year.",
    "Which direction will money go over time?",
    -1));
activities1.push(new MultipleChoiceActivity(
    "Experts warn not to move all your savings into investments. ",
    "What is one reason you think this is recommended?",
    ["Impossible to earn money from investments", "Need savings for expensive emergencies", "Investments cannot be used after retirement", "Not allowed to invest money without keeping money in savings"],
    2));
lessons.push(new Lesson("Welcome to Investing", "fa-chart-line", activities1))

// Lesson 2


// Hardcoded data end

function htmlForLesson(lesson, index, fractionComplete, active) {
    colClass = "";
    circle = `<div class="lesson-circle top-margin">
        <span class="fas ${lesson.icon}"></span>
    </div>`;
    if (active == true) {
        colClass = "partially-complete";
        circle = `<a class="lesson-circle top-margin" href="/lesson/${index+1}">
        <span class="fas ${lesson.icon}"></span></a>`;
    } else if (fractionComplete == 1) {
        colClass = "complete";
    } else {
        colClass = "not-started";
    }
    return `<div class="col col-4 top-margin ${colClass}">
    ${circle}
    <h4 class="lesson-title text-center top-margin">${index+1}. ${lesson.name}</h4>
    <p class="lesson-progress text-center">${(fractionComplete * 100).toFixed(0)}% complete</p>
</div>
    `;
}

$(document).ready(function() {
    progressStr = $(".progress-span").attr("name").split(",");
    lessonsCompleted = 0 // Number(progressStr[0].substring(1));
    lessonProgress = 0 // Number(progressStr[1].substring(progressStr[1].length));

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