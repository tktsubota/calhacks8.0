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
        circle = `<a class="lesson-circle top-margin" href="/lesson-${index+1}">
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

function htmlForActivity(activity, activityIndex, lesson, lessonIndex, opacity) {
    if (activity instanceof MultipleChoiceActivity) {
        return `<div class="card" id="card-${activityIndex}">
        <div class="row justify-content-center">
            <div class="col col-10">
                <p>${ activity.text }</p>
                <p><b>${ activity.question }</b></p>
            </div>
        </div>
        <div class="row justify-content-center mult-choice-row">
            <div class="col col-5 d-grid">
                <button class="btn multiple-choice-btn"><a class='button-link'>${ activity.options[0] }</a></button>
            </div>
            <div class="col col-5 d-grid">
                <button class="btn multiple-choice-btn"><a class='button-link'>${ activity.options[1] }</a></button>
            </div>
        </div>
        <div class="row justify-content-center mult-choice-row">
            <div class="col col-5 d-grid">
                <button class="btn multiple-choice-btn"><a class='button-link'>${ activity.options[2] }</a></button>
            </div>
            <div class="col col-5 d-grid">
                <button class="btn multiple-choice-btn"><a class='button-link'>${ activity.options[3] }</a></button>
            </div>
        </div>
    </div>`
    } else if (activity instanceof GraphActivity) {

    } else {
        return `<div class="card" id="card-${activityIndex}">
        <div class="row justify-content-center">
            <div class="col col-10">
                <h3 class="text-center">Lesson ${lessonIndex+1}. ${lesson.name}</h3>
                <br/>
                <p>${ activity.text }</p>
                <br/>
            </div>
            <div class="col col-auto">
                <button class="btn btn-lg dark-bg"><a class='button-link' onclick="nextActivity()">Next</a></button>
            </div>
        </div>
    </div>`;
    }
}

function nextActivity() {
    progressStr = $(".progress-span").attr("name").split(",");
    lessonsCompleted = Number(progressStr[0].substring(1));
    lessonProgress = Number(progressStr[1].substring(progressStr[1].length));
    currentLesson = lessons[lessonsCompleted];
    currentActivity = currentLesson.activities[lessonProgress];

    if (lessonProgress == currentLesson.activities.length) {
        // Complete lesson, give cash, unlock features, and exit out
        $.post("/setprogress", {'lesson':lessonsCompleted + 1, 'activity': 0}, function(result, status, jqXHR) {
            // Display popup for cash + features
            // Exit after popup
        });
    } else {
        $.post("/setprogress", {'lesson':0, 'activity':1}, function(result, status, jqXHR) {
            $(".progress-span").attr("name", `[${ lessonsCompleted }, ${ lessonProgress + 1 }]`);
            
            newHTML = htmlForActivity(currentLesson.activities[lessonProgress + 1], lessonProgress + 1, currentLesson, lessonsCompleted);
            $(`#card-${lessonProgress}`).animate({
                right: "+=1000px"
            }, 250, function() {
                $(`#card-${lessonProgress}`).remove();
                $(`#card-holder`).append(newHTML);
                $(`$card-${lessonProgress + 1}`).css("left", "+=1000px");
                $(`#card-${lessonProgress + 1}`).animate({
                    left: "-=1000px"
                }, 250, function() {});
            });
            percent = Number((lessonProgress + 1) * 100 / currentLesson.activities.length);
            percentStr = `${ percent }%`;
            $("#progress").animate({
                width: percentStr
            }, 500, function() {
                $("#progress").text(percentStr);
            });
        });
    }
}