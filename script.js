
/* ==========================================
   PLACEMENTOR AI - COMPLETE JAVASCRIPT
   ========================================== */

const API_URL = "http://127.0.0.1:5000";

// Assessment results for the current page session.
// null means the assessment has not been completed.
const assessment = {
    resume: null,
    interview: null,
    aptitude: null
};


// ==========================================
// 1. APTITUDE QUESTION BANK
// ==========================================

const questions = [
    {category:"Quantitative",question:"What is 20% of 250?",options:["25","40","50","60"],answer:"50"},
    {category:"Quantitative",question:"If a train travels 60 km in 1.5 hours, what is speed?",options:["30 km/h","40 km/h","45 km/h","60 km/h"],answer:"40 km/h"},
    {category:"Quantitative",question:"Find the average of 10, 20, 30, 40.",options:["20","25","30","35"],answer:"25"},
    {category:"Quantitative",question:"If cost price is 100 and selling price is 120, profit is?",options:["10","20","30","40"],answer:"20"},
    {category:"Quantitative",question:"12 × 8 = ?",options:["86","92","96","108"],answer:"96"},

    {category:"Reasoning",question:"Find next number: 2, 4, 8, 16, ?",options:["20","24","30","32"],answer:"32"},
    {category:"Reasoning",question:"If CAT is coded as DBU, DOG is coded as?",options:["EPH","EPI","FPH","EOG"],answer:"EPH"},
    {category:"Reasoning",question:"Odd one out: Apple, Mango, Carrot, Banana",options:["Apple","Mango","Carrot","Banana"],answer:"Carrot"},
    {category:"Reasoning",question:"If A=1, B=2, then D=?",options:["2","3","4","5"],answer:"4"},
    {category:"Reasoning",question:"Which comes next: Monday, Tuesday, Wednesday, ?",options:["Friday","Sunday","Thursday","Saturday"],answer:"Thursday"},

    {category:"Verbal",question:"Choose synonym of Quick.",options:["Slow","Fast","Weak","Late"],answer:"Fast"},
    {category:"Verbal",question:"Choose correct spelling.",options:["Recieve","Receive","Receeve","Receve"],answer:"Receive"},
    {category:"Verbal",question:"Opposite of Strong is?",options:["Powerful","Weak","Hard","Tall"],answer:"Weak"},
    {category:"Verbal",question:"Fill in: She ___ going to college.",options:["is","are","am","were"],answer:"is"},
    {category:"Verbal",question:"Plural of child is?",options:["Childs","Children","Childes","Childrens"],answer:"Children"},

    {category:"Technical",question:"Which concept supports code reusability in OOP?",options:["Inheritance","Loop","Array","Index"],answer:"Inheritance"},
    {category:"Technical",question:"Which language is used to query databases?",options:["HTML","CSS","SQL","XML"],answer:"SQL"},
    {category:"Technical",question:"HTML is used for?",options:["Styling","Structure","Database","Server"],answer:"Structure"},
    {category:"Technical",question:"CSS is used for?",options:["Styling","Logic","Database","Compilation"],answer:"Styling"},
    {category:"Technical",question:"Which is a programming language?",options:["Java","HTML","CSS","SQL Table"],answer:"Java"}
];


// ==========================================
// 2. HELPER FUNCTIONS
// ==========================================

function showElement(element) {
    if (!element) return;
    element.hidden = false;
    element.classList.remove("hidden");
}

function hideElement(element) {
    if (!element) return;
    element.hidden = true;
    element.classList.add("hidden");
}

function goToSection(id) {
    const section = document.getElementById(id);

    if (section) {
        showElement(section);
        section.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
}

function setText(id, value) {
    const element = document.getElementById(id);
    if (element) element.textContent = value;
}

function scoreLabel(score) {
    return score === null ? "--" : `${score.toFixed(2)}%`;
}

function updateReadinessInputs() {
    setText(
        "readinessResumeScore",
        scoreLabel(assessment.resume)
    );

    setText(
        "readinessInterviewScore",
        scoreLabel(assessment.interview)
    );

    setText(
        "readinessAptitudeScore",
        assessment.aptitude === null
            ? "Not Taken"
            : `${assessment.aptitude.toFixed(0)}%`
    );

    // An earlier prediction is stale after new results.
    hideElement(document.getElementById("readinessResults"));
    setText("readinessStatus", "");
}


// ==========================================
// 3. LOGIN
// ==========================================

function login() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const msg = document.getElementById("loginMsg");

    if (!email || !password) {
        msg.style.color = "red";
        msg.textContent = "Please enter both email and password.";
        return;
    }

    // Demonstration login only; not real authentication.
    msg.style.color = "green";
    msg.textContent = "Login successful! Student portal opened.";

    showElement(document.getElementById("studentPortal"));

    loadQuiz();
    updateReadinessInputs();

    setTimeout(() => {
        goToSection("studentPortal");
    }, 300);
}


// ==========================================
// 4. OPTIONAL APTITUDE TEST
// ==========================================

function openAptitude() {
    goToSection("aptitude");
}

function loadQuiz() {
    const quizBox = document.getElementById("quizBox");

    if (!quizBox) return;

    quizBox.replaceChildren();

    questions.forEach((q, index) => {
        const container = document.createElement("div");
        container.className = "quiz-question";

        const heading = document.createElement("h3");
        heading.textContent =
            `${index + 1}. [${q.category}] ${q.question}`;

        container.appendChild(heading);

        q.options.forEach(option => {
            const label = document.createElement("label");
            const radio = document.createElement("input");

            radio.type = "radio";
            radio.name = `q${index}`;
            radio.value = option;

            label.append(radio, document.createTextNode(" " + option));
            container.appendChild(label);
        });

        quizBox.appendChild(container);
    });
}

function submitTest() {
    let score = 0;
    let answered = 0;

    const categoryScores = {
        Quantitative: {correct:0,total:0},
        Reasoning: {correct:0,total:0},
        Verbal: {correct:0,total:0},
        Technical: {correct:0,total:0}
    };

    questions.forEach((q, index) => {
        categoryScores[q.category].total++;

        const selected = document.querySelector(
            `input[name="q${index}"]:checked`
        );

        if (selected) {
            answered++;

            if (selected.value === q.answer) {
                score++;
                categoryScores[q.category].correct++;
            }
        }
    });

    if (answered !== questions.length) {
        alert(
            `Please answer all 20 questions. ` +
            `You have answered ${answered}.`
        );
        return;
    }

    const percentage = Math.round(
        (score / questions.length) * 100
    );

    assessment.aptitude = percentage;

    setText("scoreDisplay", `${score}/${questions.length}`);
    setText("percentageDisplay", `${percentage}%`);

    let level = "Needs Practice";

    if (percentage >= 75) {
        level = "Strong Aptitude Performance";
    } else if (percentage >= 50) {
        level = "Intermediate";
    }

    setText("levelDisplay", level);

    const weakArea = findWeakArea(categoryScores);

    setText("weakAreaDisplay", weakArea);
    setText(
        "suggestionText",
        getSuggestion(weakArea, percentage)
    );

    updateReadinessInputs();

    document.querySelector(".dashboard")
        .scrollIntoView({behavior:"smooth"});
}

function findWeakArea(categoryScores) {
    let weakest = "";
    let lowest = Infinity;

    for (const category in categoryScores) {
        const data = categoryScores[category];
        const percentage = data.correct / data.total * 100;

        if (percentage < lowest) {
            lowest = percentage;
            weakest = category;
        }
    }

    return weakest;
}

function getSuggestion(weakArea, percentage) {
    if (percentage >= 75) {
        return `Good aptitude performance! Continue revising ${weakArea}.`;
    }

    const suggestions = {
        Quantitative:
            "Practice percentages, averages, profit and loss, and speed-distance questions.",
        Reasoning:
            "Practice number series, coding-decoding and logical puzzles.",
        Verbal:
            "Improve grammar, vocabulary and reading comprehension.",
        Technical:
            "Revise OOP, DBMS, SQL, Java and DSA."
    };

    return suggestions[weakArea] ||
        "Practice regularly and attempt more tests.";
}


// ==========================================
// 5. ADMIN PANEL
// ==========================================

function addAdminItem() {
    const input = document.getElementById("adminInput");
    const list = document.getElementById("adminList");

    if (!input || !list) return;

    const value = input.value.trim();

    if (!value) {
        alert("Please enter an item.");
        return;
    }

    const li = document.createElement("li");
    li.textContent = value;
    list.appendChild(li);

    input.value = "";
}


// ==========================================
// 6. AI RESUME ANALYZER
// ==========================================

async function analyzeResume() {
    const fileInput = document.getElementById("resumeFile");
    const status = document.getElementById("resumeStatus");
    const results = document.getElementById("resumeResults");
    const jobMatches = document.getElementById("jobMatches");

    const file = fileInput.files[0];

    if (!file) {
        status.textContent = "Please select a PDF resume.";
        return;
    }

    if (!file.name.toLowerCase().endsWith(".pdf")) {
        status.textContent = "Only PDF files are allowed.";
        return;
    }

    if (file.size > 5 * 1024 * 1024) {
        status.textContent = "PDF must be smaller than 5 MB.";
        return;
    }

    status.style.color = "#1e3a8a";
    status.textContent = "Analyzing resume using AI...";

    hideElement(results);
    jobMatches.replaceChildren();

    // Clear previous resume score while processing.
    assessment.resume = null;
    updateReadinessInputs();

    const formData = new FormData();
    formData.append("resume", file);

    try {
        const response = await fetch(
            `${API_URL}/analyze-resume`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Resume analysis failed.");
        }

        const matches = data.matches || [];

        status.style.color = "green";
        status.textContent = "Resume analyzed successfully!";

        if (matches.length === 0) {
            jobMatches.textContent = "No job matches found.";
        } else {
            // The best match becomes the readiness input.
            assessment.resume = Math.max(
                0,
                Math.min(
                    100,
                    ...matches.map(job => Number(job.similarity) || 0)
                )
            );

            updateReadinessInputs();

            matches.forEach(job => {
                createJobMatchCard(job, jobMatches);
            });
        }

        showElement(results);

        results.scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {
        status.style.color = "red";
        status.textContent = error.message;
    }
}


// ==========================================
// 7. JOB MATCH + CAREER ROADMAP
// ==========================================

function createJobMatchCard(job, container) {
    const card = document.createElement("div");
    card.className = "ai-match-card";

    const title = document.createElement("h3");
    title.textContent = job.role;

    const similarity = document.createElement("p");
    similarity.textContent =
        `Semantic similarity: ${job.similarity}%`;

    const progress = document.createElement("div");
    progress.className = "match-progress";

    const fill = document.createElement("div");
    fill.className = "match-progress-fill";

    fill.style.width =
        `${Math.max(0, Math.min(100, Number(job.similarity) || 0))}%`;

    progress.appendChild(fill);

    const matchedSkills = job.matched_skills || [];
    const missingSkills = job.missing_skills || [];

    const matched = document.createElement("p");
    matched.className = "matched";
    matched.textContent =
        "Matched skills: " +
        (matchedSkills.join(", ") || "None identified");

    const missing = document.createElement("p");
    missing.className = "missing";
    missing.textContent =
        "Skills to develop: " +
        (missingSkills.join(", ") || "No gaps identified");

    const roadmapButton = document.createElement("button");
    roadmapButton.type = "button";
    roadmapButton.className = "main-btn";
    roadmapButton.textContent = "Generate My Career Roadmap";

    const roadmapBox = document.createElement("div");
    roadmapBox.className = "career-roadmap";
    roadmapBox.hidden = true;

    const interviewButton = document.createElement("button");
    interviewButton.type = "button";
    interviewButton.className = "main-btn";
    interviewButton.textContent = "Start Interview Practice";
    interviewButton.hidden = true;

    roadmapButton.addEventListener("click", () => {
        roadmapBox.replaceChildren();

        const heading = document.createElement("h4");
        heading.textContent = `Career Roadmap: ${job.role}`;
        roadmapBox.appendChild(heading);

        if (missingSkills.length === 0) {
            const message = document.createElement("p");
            message.textContent =
                "Focus on projects, coding practice and interview preparation.";
            roadmapBox.appendChild(message);
        } else {
            const list = document.createElement("ol");

            missingSkills.forEach((skill, index) => {
                const item = document.createElement("li");
                item.textContent =
                    `Week ${index + 1}: Learn ${skill}, ` +
                    "practice exercises and build a small project.";
                list.appendChild(item);
            });

            const finalStep = document.createElement("li");
            finalStep.textContent =
                "Final week: Build a portfolio project, " +
                "update your resume and practice interviews.";

            list.appendChild(finalStep);
            roadmapBox.appendChild(list);
        }

        roadmapBox.hidden = false;
        interviewButton.hidden = false;

        roadmapBox.scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });
    });

    interviewButton.addEventListener("click", () => {
        goToSection("ai-interview");
    });

    card.append(
        title,
        similarity,
        progress,
        matched,
        missing,
        roadmapButton,
        roadmapBox,
        interviewButton
    );

    container.appendChild(card);
}


// ==========================================
// 8. AI INTERVIEW QUESTION LOADING
// ==========================================

async function loadInterviewQuestions() {
    const select = document.getElementById("interviewQuestion");
    if (!select) return;

    try {
        const response = await fetch(
            `${API_URL}/interview-questions`
        );

        if (!response.ok) {
            throw new Error("Unable to load interview questions.");
        }

        const interviewQuestions = await response.json();

        select.replaceChildren();

        interviewQuestions.forEach(question => {
            const option = document.createElement("option");
            option.value = question.id;
            option.textContent =
                question.category
                    ? `[${question.category}] ${question.question}`
                    : question.question;

            select.appendChild(option);
        });

        setText(
            "interviewStatus",
            `${interviewQuestions.length} questions available.`
        );

    } catch (error) {
        setText(
            "interviewStatus",
            "Unable to load questions. Check Flask backend."
        );
    }
}


// ==========================================
// 9. AI INTERVIEW ANSWER EVALUATION
// ==========================================

async function submitInterviewAnswer() {
    const select = document.getElementById("interviewQuestion");
    const answerBox = document.getElementById("interviewAnswer");
    const feedback = document.getElementById("interviewFeedback");

    const questionId = Number(select.value);
    const answer = answerBox.value.trim();

    feedback.replaceChildren();

    if (!questionId) {
        setText("interviewStatus", "Please select a question.");
        return;
    }

    if (answer.length < 15) {
        setText(
            "interviewStatus",
            "Please write a more detailed answer."
        );
        return;
    }

    setText("interviewStatus", "Evaluating your answer...");

    try {
        const response = await fetch(
            `${API_URL}/evaluate-interview`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question_id: questionId,
                    answer: answer
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Evaluation failed.");
        }

        const similarity = Number(data.similarity);

        if (!Number.isFinite(similarity)) {
            throw new Error("Invalid interview score received.");
        }

        // Store the latest completed interview result.
        assessment.interview = Math.max(
            0,
            Math.min(100, similarity)
        );

        updateReadinessInputs();

        setText("interviewStatus", "Evaluation completed!");

        const heading = document.createElement("h3");
        heading.textContent =
            `Semantic Similarity: ${data.similarity}%`;

        const covered = document.createElement("p");
        covered.textContent =
            "Concepts covered: " +
            ((data.covered_concepts || []).join(", ") ||
             "None identified");

        const missing = document.createElement("p");
        missing.textContent =
            "Suggested concepts: " +
            ((data.suggested_concepts || []).join(", ") ||
             "None");

        const message = document.createElement("p");
        message.textContent = data.feedback || "";

        const note = document.createElement("p");
        note.textContent =
            "Similarity measures semantic closeness, " +
            "not guaranteed factual correctness.";

        feedback.append(
            heading,
            covered,
            missing,
            message,
            note
        );

        const readinessButton = document.createElement("button");
        readinessButton.type = "button";
        readinessButton.className = "main-btn";
        readinessButton.textContent =
            "Continue to Placement Readiness Analysis";

        readinessButton.addEventListener("click", () => {
            goToSection("placement-readiness");
        });

        feedback.appendChild(readinessButton);

    } catch (error) {
        setText("interviewStatus", error.message);
    }
}


// ==========================================
// 10. MLP PLACEMENT READINESS ANALYSIS
// ==========================================

async function calculateReadiness() {
    const status = document.getElementById("readinessStatus");
    const results = document.getElementById("readinessResults");
    const suggestionsList =
        document.getElementById("readinessSuggestions");

    hideElement(results);

    // Resume and interview scores are required by
    // the trained MLP. Aptitude remains optional.
    if (
        assessment.resume === null ||
        assessment.interview === null
    ) {
        const missing = [];

        if (assessment.resume === null) {
            missing.push("analyze your resume");
        }

        if (assessment.interview === null) {
            missing.push("complete an AI interview question");
        }

        status.style.color = "red";
        status.textContent =
            "Please " + missing.join(" and ") +
            " before calculating readiness.";

        return;
    }

    status.style.color = "#1e3a8a";
    status.textContent =
        "Calculating experimental readiness using the MLP model...";

    const payload = {
        resume_score: assessment.resume,
        interview_score: assessment.interview,
        aptitude_score: assessment.aptitude
    };

    try {
        const response = await fetch(
            `${API_URL}/predict-readiness`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Readiness prediction failed."
            );
        }

        setText(
            "readinessScore",
            `${data.readiness_score} / 100`
        );

        setText(
            "readinessLevel",
            data.readiness_level
        );

        setText(
            "readinessDisclaimer",
            data.disclaimer ||
            "Experimental score based on simulated data. " +
            "Not an actual placement probability."
        );

        suggestionsList.replaceChildren();

        (data.suggestions || []).forEach(suggestion => {
            const item = document.createElement("li");
            item.textContent = suggestion;
            suggestionsList.appendChild(item);
        });

        status.style.color = "green";
        status.textContent =
            "Placement readiness analysis completed!";

        showElement(results);

        results.scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });

    } catch (error) {
        status.style.color = "red";
        status.textContent = error.message;
    }
}


// ==========================================
// 11. PAGE INITIALIZATION
// ==========================================

document.addEventListener("DOMContentLoaded", () => {
    hideElement(document.getElementById("aptitude"));
    hideElement(document.getElementById("studentPortal"));
    hideElement(document.getElementById("resumeResults"));
    hideElement(document.getElementById("readinessResults"));

    updateReadinessInputs();
    loadInterviewQuestions();
});
