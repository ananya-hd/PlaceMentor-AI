
import os
import sqlite3

from datetime import timedelta
from functools import wraps

from flask import Flask, jsonify, request, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

import fitz

from resume_matcher import (
    match_resume,
    INTERVIEW_QUESTIONS,
    evaluate_interview_answer
)

from readiness_model import predict_readiness


# ==========================================
# FLASK CONFIGURATION
# ==========================================

app = Flask(__name__)

IS_PRODUCTION = os.environ.get("RENDER") == "true"
# Set a permanent SECRET_KEY environment variable
# before using this outside local development.
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "local-development-only-change-this-secret"
)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=1)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = IS_PRODUCTION
app.config["SESSION_COOKIE_SAMESITE"] = (
    "None" if IS_PRODUCTION else "Lax"
)

allowed_origins = [
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5501",
    "http://localhost:5500",
    "http://localhost:5501"
]
# Allow local Live Server frontend.
frontend_url = os.environ.get("FRONTEND_URL", "").rstrip("/")

if frontend_url:
    allowed_origins.append(frontend_url)
# Use 127.0.0.1 consistently for both frontend and backend.
CORS(
    app,
    resources={
        r"/*": {
            "origins": allowed_origins
        }
    },
    supports_credentials=True
)

DATABASE = os.environ.get(
    "DATABASE_PATH",
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "students.db"
    )
)

# ==========================================
# DATABASE SETUP
# ==========================================

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


initialize_database()


# ==========================================
# AUTHENTICATION HELPER
# ==========================================

def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "student_id" not in session:
            return jsonify({
                "error": "Please login to continue."
            }), 401

        return function(*args, **kwargs)

    return wrapper


# ==========================================
# HOME
# ==========================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "PlaceMentor AI Backend Running Successfully!"
    })


# ==========================================
# STUDENT REGISTRATION
# ==========================================

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name") or "").strip()
    email = str(data.get("email") or "").strip().lower()
    password = str(data.get("password") or "")
    confirm_password = str(
        data.get("confirm_password") or ""
    )

    if not name or not email or not password:
        return jsonify({
            "error": "Name, email and password are required."
        }), 400

    if len(name) > 100 or len(email) > 254 or "@" not in email:
        return jsonify({
            "error": "Please enter a valid name and email."
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must contain at least 8 characters."
        }), 400

    if len(password) > 128:
        return jsonify({
            "error": "Password is too long."
        }), 400

    if password != confirm_password:
        return jsonify({
            "error": "Passwords do not match."
        }), 400

    password_hash = generate_password_hash(password)

    try:
        with get_db_connection() as connection:
            connection.execute(
                """
                INSERT INTO students
                (name, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (name, email, password_hash)
            )

        return jsonify({
            "message": "Registration successful! Please login."
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "An account with this email already exists."
        }), 409


# ==========================================
# STUDENT LOGIN
# ==========================================

@app.route("/login", methods=["POST"])
def student_login():
    data = request.get_json(silent=True) or {}

    email = str(data.get("email") or "").strip().lower()
    password = str(data.get("password") or "")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required."
        }), 400

    with get_db_connection() as connection:
        student = connection.execute(
            "SELECT * FROM students WHERE email = ?",
            (email,)
        ).fetchone()

    if student is None or not check_password_hash(
        student["password_hash"],
        password
    ):
        return jsonify({
            "error": "Incorrect email or password."
        }), 401

    session.clear()
    session.permanent = True

    session["student_id"] = student["id"]
    session["student_name"] = student["name"]

    return jsonify({
        "message": "Login successful!",
        "student": {
            "id": student["id"],
            "name": student["name"],
            "email": student["email"]
        }
    })


# ==========================================
# CHECK LOGIN SESSION
# ==========================================

@app.route("/me", methods=["GET"])
@login_required
def current_student():
    with get_db_connection() as connection:
        student = connection.execute(
            """
            SELECT id, name, email
            FROM students
            WHERE id = ?
            """,
            (session["student_id"],)
        ).fetchone()

    if student is None:
        session.clear()
        return jsonify({
            "error": "Student account not found."
        }), 401

    return jsonify({
        "student": dict(student)
    })


# ==========================================
# STUDENT LOGOUT
# ==========================================

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "message": "Logged out successfully."
    })


# ==========================================
# AI RESUME ANALYZER
# ==========================================

@app.route("/analyze-resume", methods=["POST"])
def analyze_resume():

    if "resume" not in request.files:
        return jsonify({
            "error": "No resume uploaded"
        }), 400

    file = request.files["resume"]

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({
            "error": "Upload a PDF resume"
        }), 400

    try:
        pdf_bytes = file.read()

        with fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        ) as document:

            if document.needs_pass:
                return jsonify({
                    "error": "Password-protected PDFs are not supported"
                }), 400

            resume_text = "\n".join(
                page.get_text()
                for page in document
            )

        if not resume_text.strip():
            return jsonify({
                "error": "No readable text found in PDF"
            }), 400

        results = match_resume(resume_text)

        return jsonify({
            "message": "Resume analyzed successfully",
            "matches": results
        })

    except Exception:
        app.logger.exception("Resume analysis failed")

        return jsonify({
            "error": "Unable to analyze this PDF"
        }), 500


# ==========================================
# AI INTERVIEW QUESTIONS
# ==========================================

@app.route("/interview-questions", methods=["GET"])
def interview_questions():

    questions = [
        {
            "id": q["id"],
            "category": q["category"],
            "question": q["question"]
        }
        for q in INTERVIEW_QUESTIONS
    ]

    return jsonify(questions)


# ==========================================
# AI INTERVIEW EVALUATION
# ==========================================

@app.route("/evaluate-interview", methods=["POST"])
def evaluate_interview():

    data = request.get_json(silent=True) or {}

    try:
        question_id = int(
            data.get("question_id", 0)
        )

        answer = str(
            data.get("answer", "")
        )

        result = evaluate_interview_answer(
            question_id,
            answer
        )

        return jsonify(result)

    except (ValueError, TypeError) as error:
        return jsonify({
            "error": str(error)
        }), 400

    except Exception:
        app.logger.exception("Interview evaluation failed")

        return jsonify({
            "error": "Evaluation failed"
        }), 500


# ==========================================
# PLACEMENT READINESS ANALYSIS
# ==========================================

@app.route("/predict-readiness", methods=["POST"])
def readiness_prediction():

    data = request.get_json(silent=True) or {}

    try:
        if (
            "resume_score" not in data
            or "interview_score" not in data
        ):
            raise ValueError(
                "Resume and interview scores are required."
            )

        result = predict_readiness(
            resume_score=data["resume_score"],
            interview_score=data["interview_score"],
            aptitude_score=data.get("aptitude_score")
        )

        return jsonify(result)

    except (ValueError, TypeError) as error:
        return jsonify({
            "error": str(error)
        }), 400

    except Exception:
        app.logger.exception("Readiness prediction failed")

        return jsonify({
            "error": "Readiness prediction failed"
        }), 500


# ==========================================
# START FLASK SERVER
# ==========================================

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
