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
activities2 = []
activities1.push(new Activity("In this lesson, you will learn more about stocks."));
activities2.push(new MultipleChoiceActivity(
    "When a company decides to go public, individuals purchase shares of the company for money.",
    "Why would a company want to give a part of their company away?",
    ["Raise money to expand the company", "Raise awareness of their company", "Required by the US Government", "Raise money for charity"],
    1));
activities2.push(new MultipleChoiceActivity(
    "A company can decide to join a stock exchange to make it easier for individuals to purchase their stock. Some examples are NASDAQ(for tech companies) and NYSE(largest stock exchange).",
    "Which of the following companies is in the NASDAQ stock exchange?",
    ["Adidas","Ford", "Amazon", "Virgin Galactic"]
    2));
activities2.push(new GraphActivity(
    "The price of a stock is determined by how much investors are willing to buy and sell the stock based on how valuable they believe the company is.",
    "If a company recently had a 50% increase in total sales over the last month, which direction should its stock price go?",
    1));
activities2.push(new MultipleChoiceActivity(
    "The graph of a stock price over time is one way of seeing the current value of a stock.",
    "The pandemic had a massive impact on many companies. Look up a graph of Amazon's 3 year stock price. How did Amazon do during the pandemic?",
    ["Become extremely valuable", "Become slightly more valuable", "Become slightly less valuable", "Become worthless"],
    1));
lessons.push(new Lesson("Introduction to Stocks", "chart-line",activities2));

//Lesson 3
activities3 = []
activities3.push(new MultipleChoiceActivity(
    "By buying portions of a company, you can earn a part of the profits of the company. The amount of money given for each stock is known as the dividend.",
    "If the annual dividend of a company is $1 and you own 23 stocks of the company, how much money did you make in dividends?",
    ["$1","$12","$23","$46"],
    2));
lessons.push(new Lesson("Advanced Stock Market Indicators", "chart-mixed",activities3));

//Lesson 4-
lessons.push(new Lesson("Mutual Funds", "chart-pie",[]));
lessons.push(new Lesson("Introduction to Cryptocurrency", "btc",[]));
lessons.push(new Lesson("Middle of Cryptocurrency", "ethereum",[]));
lessons.push(new Lesson("Final Cryptocurrency", "litecoin-sign",[]));
lessons.push(new Lesson("Future Investing", "comment-dollar",[]));

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
