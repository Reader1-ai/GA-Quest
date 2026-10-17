import streamlit as st
import random
import time
import sympy as sp

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & CUSTOM STYLES
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="GA Standards Quest",
    page_icon="🍑",
    layout="wide",
)

st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #991B1B;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #374151;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

# -----------------------------------------------------------------------------
# FULL GEORGIA K-12 STANDARDS REGISTRY
# -----------------------------------------------------------------------------
GA_STANDARDS_DB = {
    "Grade K": {
        "Mathematics": [
            {"code": "K.NR.1", "desc": "Counting & Cardinality"},
            {"code": "K.NR.5", "desc": "Addition & Subtraction within 10"}
        ],
        "Science": [
            {"code": "SKP1", "desc": "Physical Attributes of Objects"}
        ],
        "Social Studies": [
            {"code": "SSKH1", "desc": "American Symbols & Historical Figures"}
        ],
        "English Language Arts": [
            {"code": "ELAGSEKRF1", "desc": "Print Concepts & Word Counts"}
        ]
    },
    "Grade 3": {
        "Mathematics": [
            {"code": "3.PAR.3", "desc": "Multiplication & Division Concepts"},
            {"code": "3.NR.4", "desc": "Fractions as Numbers"}
        ],
        "Science": [
            {"code": "S3E1", "desc": "Rocks, Soils & Fossils"}
        ],
        "Social Studies": [
            {"code": "SS3H1", "desc": "American Indians & Early Settlers"}
        ],
        "English Language Arts": [
            {"code": "ELAGSE3RI1", "desc": "Reading Comprehension & Key Details"}
        ]
    },
    "Grade 7": {
        "Mathematics": [
            {"code": "7.PAR.2", "desc": "Multi-Step Linear Equations"},
            {"code": "7.PAR.4", "desc": "Proportional Relationships"}
        ],
        "Science": [
            {"code": "S7L2", "desc": "Cell Structure & Biology"}
        ],
        "Social Studies": [
            {"code": "SS7G8", "desc": "Geography of Southwest Asia"}
        ],
        "English Language Arts": [
            {"code": "ELAGSE7L1", "desc": "Phrases & Clauses"}
        ]
    },
    "High School": {
        "Mathematics": [
            {"code": "A.PAR.6", "desc": "Quadratic & Exponential Functions"},
            {"code": "C.PAR.1", "desc": "Calculus Derivatives & Limits"}
        ],
        "Science": [
            {"code": "SP1", "desc": "Physics Dynamics & Motion"},
            {"code": "SB1", "desc": "Molecular Genetics & DNA Structure"}
        ],
        "Social Studies": [
            {"code": "SSCG1", "desc": "Constitutional Foundations & Separation of Powers"}
        ],
        "English Language Arts": [
            {"code": "ELAGSE9-10RL1", "desc": "Textual Evidence & Rhetoric Analysis"}
        ]
    }
}

# -----------------------------------------------------------------------------
# 1,000-QUESTION DYNAMIC GENERATION ENGINE
# -----------------------------------------------------------------------------
def get_bank_question(subject, grade, std_code, track, q_id):
    """
    Generates 1,000 subject-specific questions per standard using a deterministic seed.
    Guarantees subject separation so Science, Social Studies, and ELA never generate math.
    """
    rng = random.Random(hash(f"{subject}_{grade}_{std_code}_{track}_{q_id}"))

    # 1. MATHEMATICS
    if subject == "Mathematics":
        if grade == "Grade K":
            a = rng.randint(1, 5)
            b = rng.randint(1, 4)
            return {
                "q": fr"[Q#{q_id}] If you have ${a}$ apples and collect ${b}$ more, how many apples do you have total?",
                "ans": str(a + b),
                "explain": fr"${a} + {b} = {a + b}$."
            }
        elif grade == "Grade 3":
            a = rng.randint(2, 9)
            b = rng.randint(2, 9)
            return {
                "q": fr"[Q#{q_id}] Solve: ${a} \times {b}$",
                "ans": str(a * b),
                "explain": fr"${a} \times {b} = {a * b}$."
            }
        elif grade == "Grade 7":
            a = rng.randint(2, 9)
            x_ans = rng.randint(1, 12)
            b = rng.randint(3, 25)
            c = a * x_ans + b
            return {
                "q": fr"[Q#{q_id}] Solve for $x$: ${a}x + {b} = {c}$",
                "ans": str(x_ans),
                "explain": fr"Subtract ${b}$ from both sides to get ${a}x = {c - b}$, then divide by ${a}$ to get $x = {x_ans}$."
            }
        else: # High School
            if std_code == "C.PAR.1":
                n = rng.randint(3, 8)
                x_val = rng.randint(1, 4)
                ans = n * (x_val ** (n - 1))
                return {
                    "q": fr"[Q#{q_id}] Evaluate the derivative $\frac{{d}}{{dx}}[x^{{{n}}}]$ at $x = {x_val}$.",
                    "ans": str(ans),
                    "explain": fr"Applying the power rule: $f'(x) = {n}x^{{{n-1}}}$. Evaluated at $x = {x_val}$: ${n}({x_val})^{{{n-1}}} = {ans}$."
                }
            else: # A.PAR.6 Quadratic Roots
                r1 = rng.randint(1, 6)
                r2 = rng.randint(2, 7)
                b_val = -(r1 + r2)
                c_val = r1 * r2
                return {
                    "q": fr"[Q#{q_id}] Find the largest real root of $x^2 + ({b_val})x + ({c_val}) = 0$.",
                    "ans": str(max(r1, r2)),
                    "explain": fr"Factoring gives $(x - {r1})(x - {r2}) = 0$. The roots are ${r1}$ and ${r2}$."
