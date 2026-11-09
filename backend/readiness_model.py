
import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "readiness_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "readiness_scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


def predict_readiness(resume_score, interview_score, aptitude_score=None):
    """
    Generate an experimental placement preparation score.

    This model was trained on simulated data, so its
    output is not an actual placement probability.
    """

    resume_score = float(resume_score)
    interview_score = float(interview_score)

    if not (0 <= resume_score <= 100):
        raise ValueError("Resume score must be between 0 and 100.")

    if not (0 <= interview_score <= 100):
        raise ValueError("Interview score must be between 0 and 100.")

    if aptitude_score is None:
        aptitude_value = 50.0
        aptitude_taken = 0
    else:
        aptitude_value = float(aptitude_score)

        if not (0 <= aptitude_value <= 100):
            raise ValueError("Aptitude score must be between 0 and 100.")

        aptitude_taken = 1

    features = np.array([[
        resume_score,
        interview_score,
        aptitude_value,
        aptitude_taken
    ]])

    scaled_features = scaler.transform(features)

    prediction = float(model.predict(scaled_features)[0])

    prediction = round(
        max(0, min(100, prediction)),
        2
    )

    if prediction >= 75:
        level = "Strong Preparation"
    elif prediction >= 50:
        level = "Developing Preparation"
    else:
        level = "Needs Improvement"

    suggestions = []

    if resume_score < 60:
        suggestions.append(
            "Improve your resume by developing relevant "
            "technical skills and completing practical projects."
        )

    if interview_score < 60:
        suggestions.append(
            "Practice technical interview questions and "
            "improve your explanations."
        )

    if aptitude_score is None:
        suggestions.append(
            "You can optionally take the aptitude test "
            "for a more complete preparation assessment."
        )
    elif aptitude_value < 60:
        suggestions.append(
            "Practice quantitative aptitude, reasoning, "
            "verbal ability and technical fundamentals."
        )

    if not suggestions:
        suggestions.append(
            "Continue practicing interviews, building "
            "projects and strengthening your skills."
        )

    return {
        "readiness_score": prediction,
        "readiness_level": level,
        "suggestions": suggestions,
        "aptitude_included": bool(aptitude_taken),
        "model_type": "Experimental MLP neural network",
        "disclaimer": (
            "This score estimates preparation against "
            "a simulated rubric. It does not predict "
            "actual placement success."
        )
    }
