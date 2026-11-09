
/*
 * PlaceMentor AI
 * Student registration, login, logout and session handling
 */

const AUTH_API = "http://127.0.0.1:5000";

let authenticatedStudent = null;

function authShow(element) {
    if (!element) return;
    element.hidden = false;
    element.classList.remove("hidden");
}

function authHide(element) {
    if (!element) return;
    element.hidden = true;
    element.classList.add("hidden");
}

function authMessage(id, message, success = false) {
    const element = document.getElementById(id);
    if (!element) return;

    element.textContent = message;
    element.style.color = success ? "green" : "red";
}

function showRegister() {
    authHide(document.getElementById("loginForm"));
    authShow(document.getElementById("registerForm"));
    authMessage("registerMsg", "");
}

function showLogin() {
    authHide(document.getElementById("registerForm"));
    authShow(document.getElementById("loginForm"));
    authMessage("loginMsg", "");
}

async function authRequest(path, options = {}) {
    const response = await fetch(AUTH_API + path, {
        ...options,
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Request failed.");
    }

    return data;
}

async function registerStudent() {
    const name = document.getElementById("registerName").value.trim();
    const email = document.getElementById("registerEmail").value.trim();
    const password = document.getElementById("registerPassword").value;
    const confirmPassword =
        document.getElementById("confirmPassword").value;

    if (!name || !email || !password || !confirmPassword) {
        authMessage("registerMsg", "Please complete all fields.");
        return;
    }

    if (password.length < 8) {
        authMessage(
            "registerMsg",
            "Password must contain at least 8 characters."
        );
        return;
    }

    if (password !== confirmPassword) {
        authMessage("registerMsg", "Passwords do not match.");
        return;
    }

    authMessage("registerMsg", "Creating your account...", true);

    try {
        const data = await authRequest("/register", {
            method: "POST",
            body: JSON.stringify({
                name,
                email,
                password,
                confirm_password: confirmPassword
            })
        });

        document.getElementById("registerPassword").value = "";
        document.getElementById("confirmPassword").value = "";

        showLogin();

        document.getElementById("email").value = email;

        authMessage(
            "loginMsg",
            data.message || "Account created. Please log in.",
            true
        );

    } catch (error) {
        authMessage("registerMsg", error.message);
    }
}

function openAuthenticatedPortal(student) {
    authenticatedStudent = student;

    authShow(document.getElementById("studentPortal"));
    authHide(document.getElementById("login"));

    const welcome = document.getElementById("studentWelcome");

    if (welcome) {
        welcome.textContent = `Welcome, ${student.name}!`;
    }

    // These functions are provided by the existing script.js.
    if (typeof loadQuiz === "function") {
        loadQuiz();
    }

    if (typeof updateReadinessInputs === "function") {
        updateReadinessInputs();
    }
}

function resetStudentAssessments() {
    if (typeof assessment !== "undefined") {
        assessment.resume = null;
        assessment.interview = null;
        assessment.aptitude = null;
    }

    const quiz = document.getElementById("quizBox");
    if (quiz) quiz.replaceChildren();

    const jobMatches = document.getElementById("jobMatches");
    if (jobMatches) jobMatches.replaceChildren();

    const interviewAnswer = document.getElementById("interviewAnswer");
    if (interviewAnswer) interviewAnswer.value = "";

    const interviewFeedback = document.getElementById("interviewFeedback");
    if (interviewFeedback) interviewFeedback.replaceChildren();

    [
        "resumeResults",
        "readinessResults",
        "aptitude"
    ].forEach(id => authHide(document.getElementById(id)));

    const resumeFile = document.getElementById("resumeFile");
    if (resumeFile) resumeFile.value = "";

    [
        "resumeStatus",
        "interviewStatus",
        "readinessStatus"
    ].forEach(id => {
        const element = document.getElementById(id);
        if (element) element.textContent = "";
    });

    const defaults = {
        scoreDisplay: "Not Taken",
        percentageDisplay: "--",
        levelDisplay: "Not Started",
        weakAreaDisplay: "--",
        suggestionText: "Complete the aptitude test for suggestions."
    };

    Object.entries(defaults).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) element.textContent = value;
    });

    if (typeof updateReadinessInputs === "function") {
        updateReadinessInputs();
    }
}

async function login() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!email || !password) {
        authMessage("loginMsg", "Enter email and password.");
        return;
    }

    authMessage("loginMsg", "Checking credentials...", true);

    try {
        const data = await authRequest("/login", {
            method: "POST",
            body: JSON.stringify({email, password})
        });

        resetStudentAssessments();
        openAuthenticatedPortal(data.student);

        document.getElementById("password").value = "";

        document.getElementById("studentPortal").scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {
        authMessage("loginMsg", error.message);
    }
}

async function logout() {
    try {
        await authRequest("/logout", {
            method: "POST",
            body: JSON.stringify({})
        });

        authenticatedStudent = null;

        resetStudentAssessments();

        authHide(document.getElementById("studentPortal"));
        authShow(document.getElementById("login"));

        document.getElementById("password").value = "";

        showLogin();

        authMessage(
            "loginMsg",
            "Logged out successfully.",
            true
        );

        document.getElementById("login").scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {
        alert(error.message);
    }
}

async function restoreStudentSession() {
    try {
        const data = await authRequest("/me", {
            method: "GET"
        });

        openAuthenticatedPortal(data.student);

    } catch (error) {
        authenticatedStudent = null;
        authHide(document.getElementById("studentPortal"));
        authShow(document.getElementById("login"));
    }
}

document.addEventListener("DOMContentLoaded", () => {
    restoreStudentSession();
});
