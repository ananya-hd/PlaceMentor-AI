
/*
 * PlaceMentor AI
 * Subject-wise numbered interview navigation
 */

let interviewQuestionBank = [];
let filteredInterviewQuestions = [];

const interviewCategoryOrder = [
    "Python",
    "Java & OOP",
    "DSA",
    "DBMS & SQL",
    "Machine Learning",
    "Deep Learning",
    "HR",
    "Aptitude"
];

function clearInterviewAnswer() {
    const answer = document.getElementById("interviewAnswer");
    const feedback = document.getElementById("interviewFeedback");

    if (answer) answer.value = "";
    if (feedback) feedback.replaceChildren();
}

function updateInterviewPosition() {
    const select = document.getElementById("interviewQuestion");

    const position = select.selectedIndex + 1;
    const total = filteredInterviewQuestions.length;

    document.getElementById("interviewQuestionPosition")
        .textContent = total
            ? `Question ${position} of ${total}`
            : "No questions available";

    document.getElementById("previousInterviewQuestion")
        .disabled = position <= 1;

    document.getElementById("nextInterviewQuestion")
        .disabled = position >= total;

    clearInterviewAnswer();
}

function filterInterviewQuestions() {
    const category = document.getElementById(
        "interviewCategory"
    ).value;

    const select = document.getElementById(
        "interviewQuestion"
    );

    filteredInterviewQuestions = interviewQuestionBank.filter(
        question => question.category === category
    );

    select.replaceChildren();

    filteredInterviewQuestions.forEach((question, index) => {
        const option = document.createElement("option");

        // Preserve original backend question IDs.
        option.value = question.id;

        // Display numbering within each subject.
        option.textContent =
            `Q${index + 1}. ${question.question}`;

        select.appendChild(option);
    });

    document.getElementById("interviewQuestionCount")
        .textContent =
            `${category}: ${filteredInterviewQuestions.length} questions`;

    updateInterviewPosition();
}

function previousInterviewQuestion() {
    const select = document.getElementById("interviewQuestion");

    if (select.selectedIndex > 0) {
        select.selectedIndex--;
        updateInterviewPosition();
    }
}

function nextInterviewQuestion() {
    const select = document.getElementById("interviewQuestion");

    if (select.selectedIndex < select.options.length - 1) {
        select.selectedIndex++;
        updateInterviewPosition();
    }
}

/*
 * Override the original question-loading function
 * while keeping the existing AI evaluation function.
 */
window.loadInterviewQuestions = async function () {
    const categorySelect = document.getElementById(
        "interviewCategory"
    );

    const questionSelect = document.getElementById(
        "interviewQuestion"
    );

    if (!categorySelect || !questionSelect) return;

    try {
        const response = await fetch(
            "http://127.0.0.1:5000/interview-questions",
            {credentials: "include"}
        );

        if (!response.ok) {
            throw new Error("Unable to load interview questions.");
        }

        interviewQuestionBank = await response.json();

        categorySelect.replaceChildren();

        const availableCategories = [
            ...new Set(
                interviewQuestionBank.map(question => question.category)
            )
        ];

        const orderedCategories = [
            ...interviewCategoryOrder.filter(
                category => availableCategories.includes(category)
            ),
            ...availableCategories.filter(
                category => !interviewCategoryOrder.includes(category)
            )
        ];

        orderedCategories.forEach(category => {
            const option = document.createElement("option");

            option.value = category;

            const count = interviewQuestionBank.filter(
                question => question.category === category
            ).length;

            option.textContent = `${category} (${count})`;

            categorySelect.appendChild(option);
        });

        categorySelect.addEventListener(
            "change",
            filterInterviewQuestions
        );

        questionSelect.addEventListener(
            "change",
            updateInterviewPosition
        );

        if (orderedCategories.length > 0) {
            categorySelect.value = orderedCategories[0];
            filterInterviewQuestions();
        }

        document.getElementById("interviewStatus")
            .textContent =
                `${interviewQuestionBank.length} interview questions loaded.`;

    } catch (error) {
        document.getElementById("interviewStatus")
            .textContent = error.message;
    }
};
// Reload questions using the new subject-wise navigation
document.addEventListener("DOMContentLoaded", () => {
    loadInterviewQuestions();
});
