
import csv
import os
import re

from sentence_transformers import SentenceTransformer, util


# ==================================================
# PLACEMENTOR AI - RESUME MATCHING + INTERVIEW AI
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOBS_FILE = os.path.join(BASE_DIR, "jobs.csv")

# Pretrained Deep Learning sentence embedding model
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# ==================================================
# PART 1 - AI RESUME ANALYZER
# ==================================================

def load_jobs():
    """Load job descriptions from jobs.csv."""

    with open(
        JOBS_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        return list(csv.DictReader(file))


def find_skills(resume_text, skills):
    """Identify matched and missing job skills."""

    found = []
    missing = []

    for skill in skills:
        skill = skill.strip()

        if not skill:
            continue

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            resume_text,
            re.IGNORECASE
        ):
            found.append(skill)
        else:
            missing.append(skill)

    return found, missing


def match_resume(resume_text):
    """Compare resume with available job profiles."""

    jobs = load_jobs()

    if not jobs:
        return []

    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=True
    )

    job_descriptions = [
        job["description"]
        for job in jobs
    ]

    job_embeddings = model.encode(
        job_descriptions,
        convert_to_tensor=True
    )

    similarities = util.cos_sim(
        resume_embedding,
        job_embeddings
    )[0]

    results = []

    for index, job in enumerate(jobs):

        score = float(similarities[index])

        skills = job["skills"].split(";")

        found, missing = find_skills(
            resume_text,
            skills
        )

        results.append({
            "role": job["role"],
            "similarity": round(score * 100, 2),
            "matched_skills": found,
            "missing_skills": missing
        })

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return results


# ==================================================
# PART 2 - INTERVIEW QUESTION BANK
# ==================================================

INTERVIEW_QUESTIONS = [

    # ==============================================
    # PYTHON PROGRAMMING - 5 QUESTIONS
    # ==============================================

    {
        "id": 1,
        "category": "Python",
        "question": "What is Python and why is it popular?",
        "reference": (
            "Python is a high-level, interpreted, "
            "general-purpose programming language. "
            "It is popular because of its readable syntax, "
            "large standard library, extensive ecosystem "
            "and support for automation, web development, "
            "data science and machine learning."
        ),
        "keywords": [
            "interpreted",
            "high-level",
            "readable",
            "libraries"
        ]
    },

    {
        "id": 2,
        "category": "Python",
        "question": "What is the difference between a list and a tuple?",
        "reference": (
            "A list is mutable, meaning its elements can "
            "be changed after creation. A tuple is immutable, "
            "meaning its elements cannot be reassigned. "
            "Lists use square brackets and tuples commonly "
            "use parentheses."
        ),
        "keywords": [
            "mutable",
            "immutable",
            "list",
            "tuple"
        ]
    },

    {
        "id": 3,
        "category": "Python",
        "question": "What is a dictionary in Python?",
        "reference": (
            "A dictionary is a mutable mapping that stores "
            "data as key-value pairs. Keys are unique and "
            "hashable, and values can be accessed efficiently "
            "using their corresponding keys."
        ),
        "keywords": [
            "key",
            "value",
            "mapping",
            "mutable"
        ]
    },

    {
        "id": 4,
        "category": "Python",
        "question": "What is the difference between == and is in Python?",
        "reference": (
            "The equality operator == compares whether two "
            "objects have equal values. The is operator "
            "compares object identity, checking whether "
            "two references point to the same object."
        ),
        "keywords": [
            "equality",
            "identity",
            "value",
            "object"
        ]
    },

    {
        "id": 5,
        "category": "Python",
        "question": "What is exception handling in Python?",
        "reference": (
            "Exception handling manages runtime errors "
            "using try, except, else and finally blocks. "
            "It allows a program to respond to errors "
            "without unexpectedly terminating."
        ),
        "keywords": [
            "try",
            "except",
            "finally",
            "errors"
        ]
    },


    # ==============================================
    # JAVA AND OOP - 4 QUESTIONS
    # ==============================================

    {
        "id": 6,
        "category": "Java & OOP",
        "question": "What are the four pillars of object-oriented programming?",
        "reference": (
            "The four pillars of object-oriented programming "
            "are encapsulation, inheritance, polymorphism "
            "and abstraction. They help organize code, "
            "reuse functionality and manage complexity."
        ),
        "keywords": [
            "encapsulation",
            "inheritance",
            "polymorphism",
            "abstraction"
        ]
    },

    {
        "id": 7,
        "category": "Java & OOP",
        "question": "What is inheritance in Java?",
        "reference": (
            "Inheritance allows a class to acquire accessible "
            "fields and methods from another class. "
            "It supports code reuse and establishes "
            "an is-a relationship between classes."
        ),
        "keywords": [
            "class",
            "extends",
            "reuse",
            "inheritance"
        ]
    },

    {
        "id": 8,
        "category": "Java & OOP",
        "question": "What is polymorphism in Java?",
        "reference": (
            "Polymorphism allows the same interface or "
            "method call to have different implementations. "
            "In Java, method overloading is associated with "
            "compile-time polymorphism, while method "
            "overriding enables runtime polymorphism."
        ),
        "keywords": [
            "overloading",
            "overriding",
            "runtime",
            "method"
        ]
    },

    {
        "id": 9,
        "category": "Java & OOP",
        "question": "What is the difference between an abstract class and an interface in Java?",
        "reference": (
            "An abstract class can contain instance state, "
            "constructors, concrete methods and abstract methods. "
            "An interface defines a contract and can contain "
            "abstract, default, static and private methods. "
            "A Java class can extend one class and implement "
            "multiple interfaces."
        ),
        "keywords": [
            "abstract",
            "interface",
            "implement",
            "methods"
        ]
    },


    # ==============================================
    # DATA STRUCTURES AND ALGORITHMS - 4 QUESTIONS
    # ==============================================

    {
        "id": 10,
        "category": "DSA",
        "question": "What is the difference between an array and a linked list?",
        "reference": (
            "An array stores elements in indexed positions "
            "and supports constant-time random access. "
            "A linked list stores elements in nodes connected "
            "by references. Linked lists allow efficient "
            "insertion and deletion when the required node "
            "or position is already known."
        ),
        "keywords": [
            "array",
            "nodes",
            "access",
            "insertion"
        ]
    },

    {
        "id": 11,
        "category": "DSA",
        "question": "What is a stack and where is it used?",
        "reference": (
            "A stack is a linear data structure that follows "
            "Last In First Out, or LIFO. Its common operations "
            "are push, pop and peek. Stacks are used in "
            "function calls, undo operations and expression "
            "evaluation."
        ),
        "keywords": [
            "LIFO",
            "push",
            "pop",
            "stack"
        ]
    },

    {
        "id": 12,
        "category": "DSA",
        "question": "What is binary search and what is its time complexity?",
        "reference": (
            "Binary search finds a target in a sorted "
            "search space by repeatedly dividing the "
            "remaining interval in half. Its time "
            "complexity is O(log n)."
        ),
        "keywords": [
            "sorted",
            "half",
            "binary",
            "log"
        ]
    },

    {
        "id": 13,
        "category": "DSA",
        "question": "What is the difference between BFS and DFS?",
        "reference": (
            "Breadth First Search explores nodes level "
            "by level, typically using a queue. "
            "Depth First Search explores deeply along "
            "a path before backtracking, typically "
            "using a stack or recursion."
        ),
        "keywords": [
            "BFS",
            "DFS",
            "queue",
            "stack"
        ]
    },


    # ==============================================
    # DBMS AND SQL - 3 QUESTIONS
    # ==============================================

    {
        "id": 14,
        "category": "DBMS & SQL",
        "question": "What is a primary key in a database?",
        "reference": (
            "A primary key uniquely identifies each row "
            "in a relational database table. "
            "Its values must be unique and cannot be NULL."
        ),
        "keywords": [
            "unique",
            "NULL",
            "row",
            "primary"
        ]
    },

    {
        "id": 15,
        "category": "DBMS & SQL",
        "question": "What is the difference between INNER JOIN and LEFT JOIN?",
        "reference": (
            "INNER JOIN returns rows with matching join "
            "conditions in both tables. LEFT JOIN returns "
            "all rows from the left table and matching rows "
            "from the right table, using NULL for missing "
            "right-side values."
        ),
        "keywords": [
            "INNER",
            "LEFT",
            "matching",
            "NULL"
        ]
    },

    {
        "id": 16,
        "category": "DBMS & SQL",
        "question": "What is database normalization?",
        "reference": (
            "Database normalization organizes relational "
            "tables to reduce redundancy and avoid "
            "insertion, update and deletion anomalies. "
            "Common normal forms include first, second "
            "and third normal form."
        ),
        "keywords": [
            "redundancy",
            "normalization",
            "anomalies",
            "tables"
        ]
    },


    # ==============================================
    # MACHINE LEARNING AND DEEP LEARNING - 6
    # ==============================================

    {
        "id": 17,
        "category": "Machine Learning",
        "question": "What is the difference between supervised and unsupervised learning?",
        "reference": (
            "Supervised learning trains models using "
            "labeled examples to predict outputs. "
            "Unsupervised learning discovers patterns "
            "or structure in unlabeled data, such as "
            "clusters."
        ),
        "keywords": [
            "supervised",
            "unsupervised",
            "labeled",
            "unlabeled"
        ]
    },

    {
        "id": 18,
        "category": "Machine Learning",
        "question": "What is overfitting in machine learning?",
        "reference": (
            "Overfitting occurs when a model learns "
            "training data too closely, including noise, "
            "and generalizes poorly to unseen data. "
            "It can be reduced using regularization, "
            "early stopping and suitable validation."
        ),
        "keywords": [
            "training",
            "unseen",
            "regularization",
            "generalization"
        ]
    },

    {
        "id": 19,
        "category": "Machine Learning",
        "question": "What is the difference between classification and regression?",
        "reference": (
            "Classification predicts discrete categories "
            "or class labels, while regression predicts "
            "continuous numerical values."
        ),
        "keywords": [
            "classification",
            "regression",
            "categories",
            "continuous"
        ]
    },

    {
        "id": 20,
        "category": "Deep Learning",
        "question": "What is an artificial neural network?",
        "reference": (
            "An artificial neural network contains "
            "interconnected layers of computational "
            "units called neurons. It learns patterns "
            "by updating weights during training, "
            "often through backpropagation and "
            "gradient-based optimization."
        ),
        "keywords": [
            "layers",
            "neurons",
            "weights",
            "backpropagation"
        ]
    },

    {
        "id": 21,
        "category": "Deep Learning",
        "question": "What is a Convolutional Neural Network?",
        "reference": (
            "A Convolutional Neural Network, or CNN, "
            "is a neural network commonly used for "
            "image processing. Convolutional filters "
            "learn spatial features such as edges, "
            "textures and shapes."
        ),
        "keywords": [
            "CNN",
            "convolution",
            "filters",
            "features"
        ]
    },

    {
        "id": 22,
        "category": "Deep Learning",
        "question": "What is backpropagation in deep learning?",
        "reference": (
            "Backpropagation computes gradients of "
            "the loss with respect to neural network "
            "parameters using the chain rule. "
            "An optimizer uses these gradients "
            "to update weights and reduce loss."
        ),
        "keywords": [
            "gradients",
            "loss",
            "chain",
            "weights"
        ]
    },


    # ==============================================
    # HR INTERVIEW - 5 QUESTIONS
    # ==============================================

    {
        "id": 23,
        "category": "HR",
        "question": "Tell me about yourself.",
        "reference": (
            "A strong introduction briefly describes "
            "the candidate's education, relevant "
            "technical skills, practical projects, "
            "achievements and career goals. "
            "It should be clear, relevant and concise."
        ),
        "keywords": [
            "education",
            "skills",
            "projects",
            "goals"
        ]
    },

    {
        "id": 24,
        "category": "HR",
        "question": "Why should we hire you?",
        "reference": (
            "A strong response connects the candidate's "
            "relevant skills, projects, problem-solving "
            "abilities and willingness to learn with "
            "the requirements of the job and the "
            "value they can contribute."
        ),
        "keywords": [
            "skills",
            "projects",
            "learn",
            "contribute"
        ]
    },

    {
        "id": 25,
        "category": "HR",
        "question": "What are your strengths and weaknesses?",
        "reference": (
            "A good response identifies genuine strengths "
            "with examples and discusses a real weakness "
            "along with specific steps being taken "
            "to improve it."
        ),
        "keywords": [
            "strengths",
            "weakness",
            "improve",
            "example"
        ]
    },

    {
        "id": 26,
        "category": "HR",
        "question": "Describe a challenging project you worked on.",
        "reference": (
            "A strong response explains the project "
            "situation, the challenge, the candidate's "
            "responsibilities, actions taken and "
            "measurable or observable results. "
            "The STAR structure can help."
        ),
        "keywords": [
            "challenge",
            "project",
            "action",
            "result"
        ]
    },

    {
        "id": 27,
        "category": "HR",
        "question": "Where do you see yourself in five years?",
        "reference": (
            "A thoughtful response describes realistic "
            "career goals, continued learning, "
            "professional growth and increasing "
            "responsibility while connecting those "
            "goals to the opportunity."
        ),
        "keywords": [
            "career",
            "learning",
            "growth",
            "responsibility"
        ]
    },


    # ==============================================
    # APTITUDE AND PROBLEM SOLVING - 3 QUESTIONS
    # ==============================================

    {
        "id": 28,
        "category": "Aptitude",
        "question": "How do you calculate percentage increase?",
        "reference": (
            "Percentage increase is calculated by "
            "subtracting the original value from "
            "the new value, dividing the difference "
            "by the original nonzero value and "
            "multiplying by 100."
        ),
        "keywords": [
            "original",
            "new",
            "difference",
            "100"
        ]
    },

    {
        "id": 29,
        "category": "Aptitude",
        "question": "A train travels 120 km in 2 hours. How do you calculate its average speed?",
        "reference": (
            "Average speed equals total distance "
            "divided by total time. For a distance "
            "of 120 kilometers and time of 2 hours, "
            "the average speed is 60 kilometers "
            "per hour."
        ),
        "keywords": [
            "distance",
            "time",
            "speed",
            "60"
        ]
    },

    {
        "id": 30,
        "category": "Aptitude",
        "question": "How would you approach solving an unfamiliar logical reasoning problem?",
        "reference": (
            "First understand the problem and identify "
            "the given information and constraints. "
            "Look for patterns, break the problem into "
            "smaller steps, test possible solutions "
            "and verify the final answer."
        ),
        "keywords": [
            "patterns",
            "constraints",
            "steps",
            "verify"
        ]
    }

]


# ==================================================
# PART 3 - AI INTERVIEW ANSWER EVALUATION
# ==================================================

def evaluate_interview_answer(question_id, answer):
    """
    Evaluate a student's answer using
    Sentence Transformer semantic similarity
    and keyword-based concept coverage.
    """

    question = next(
        (
            q for q in INTERVIEW_QUESTIONS
            if q["id"] == question_id
        ),
        None
    )

    if question is None:
        raise ValueError("Invalid interview question.")

    if not isinstance(answer, str):
        raise ValueError("Answer must be text.")

    answer = answer.strip()

    if len(answer) < 15:
        raise ValueError(
            "Please write a more detailed answer."
        )

    # Generate embeddings for the student answer
    # and the reference answer.

    embeddings = model.encode(
        [
            answer,
            question["reference"]
        ],
        convert_to_tensor=True
    )

    similarity = float(
        util.cos_sim(
            embeddings[0],
            embeddings[1]
        )[0][0]
    )

    similarity_percentage = round(
        similarity * 100,
        2
    )

    # Identify concepts mentioned in the answer.

    covered = []
    missing = []

    for keyword in question["keywords"]:

        pattern = (
            r"(?<!\w)"
            + re.escape(keyword)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            answer,
            re.IGNORECASE
        ):
            covered.append(keyword)
        else:
            missing.append(keyword)

    # Generate helpful feedback.
    # This is semantic feedback, not a factual
    # correctness guarantee.

    if similarity_percentage >= 75:
        feedback = (
            "Your answer is semantically close to "
            "the reference explanation. Review "
            "the suggested concepts and ensure "
            "your statements are factually correct."
        )

    elif similarity_percentage >= 50:
        feedback = (
            "Your answer covers some relevant ideas. "
            "Try adding more detail and explaining "
            "the important concepts clearly."
        )

    else:
        feedback = (
            "Your answer has limited semantic similarity "
            "to the reference explanation. Review "
            "the topic and try answering again "
            "using your own words."
        )

    if missing:
        feedback += (
            " Suggested concepts to review: "
            + ", ".join(missing)
            + "."
        )

    return {
        "question": question["question"],
        "category": question["category"],
        "similarity": similarity_percentage,
        "covered_concepts": covered,
        "suggested_concepts": missing,
        "feedback": feedback
    }
