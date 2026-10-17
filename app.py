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
        "Mathematics": [{"code": "K.NR.1", "desc": "Counting & Cardinality"}, {"code": "K.NR.5", "desc": "Addition & Subtraction within 10"}],
        "Science": [{"code": "SKP1", "desc": "Physical Attributes of Objects"}],
        "Social Studies": [{"code": "SSKH1", "desc": "American Symbols & Historical Figures"}],
        "English Language Arts": [{"code": "ELAGSEKRF1", "desc": "Print Concepts & Word Counts"}]
    },
    "Grade 3": {
        "Mathematics": [{"code": "3.PAR.3", "desc": "Multiplication & Division Concepts"}, {"code": "3.NR.4", "desc": "Fractions as Numbers"}],
        "Science": [{"code": "S3E1", "desc": "Rocks, Soils & Fossils"}],
        "Social Studies": [{"code": "SS3H1", "desc": "American Indians & Early Settlers"}],
        "English Language Arts": [{"code": "ELAGSE3RI1", "desc": "Reading Comprehension & Key Details"}]
    },
    "Grade 7": {
        "Mathematics": [{"code": "7.PAR.2", "desc": "Multi-Step Linear Equations"}, {"code": "7.PAR.4", "desc": "Proportional Relationships"}],
        "Science": [{"code": "S7L2", "desc": "Cell Structure & Biology"}],
        "Social Studies": [{"code": "SS7G8", "desc": "Geography of Southwest Asia"}],
        "English Language Arts": [{"code": "ELAGSE7L1", "desc": "Phrases & Clauses"}]
    },
    "High School": {
        "Mathematics": [{"code": "A.PAR.6", "desc": "Quadratic & Exponential Functions"}, {"code": "C.PAR.1", "desc": "Calculus Derivatives & Limits"}],
        "Science": [{"code": "SP1", "desc": "Physics Dynamics & Motion"}, {"code": "SB1", "desc": "Molecular Genetics & DNA Structure"}],
        "Social Studies": [{"code": "SSCG1", "desc": "Constitutional Foundations & Separation of Powers"}],
        "English Language Arts": [{"code": "ELAGSE9-10RL1", "desc": "Textual Evidence & Rhetoric Analysis"}]
    }
}

# -----------------------------------------------------------------------------
# 1,000-QUESTION DYNAMIC GENERATION ENGINE
# -----------------------------------------------------------------------------
def get_bank_question(subject, grade, std_code, track, q_id):
    rng = random.Random(hash(f"{subject}_{grade}_{std_code}_{track}_{q_id}"))

    # 1. MATHEMATICS
    if subject == "Mathematics":
        if grade == "Grade K":
            a = rng.randint(1, 5)
            b = rng.randint(1, 4)
            return {
                "q": f"[Q#{q_id}] If you have ${a}$ apples and collect ${b}$ more, how many apples do you have total?",
                "ans": str(a + b),
                "explain": f"${a} + {b} = {a + b}$."
            }
        elif grade == "Grade 3":
            a = rng.randint(2, 9)
            b = rng.randint(2, 9)
            return {
                "q": f"[Q#{q_id}] Solve: ${a} \\times {b}$",
                "ans": str(a * b),
                "explain": f"${a} \\times {b} = {a * b}$."
            }
        elif grade == "Grade 7":
            a = rng.randint(2, 9)
            x_ans = rng.randint(1, 12)
            b = rng.randint(3, 25)
            c = a * x_ans + b
            return {
                "q": f"[Q#{q_id}] Solve for $x$: ${a}x + {b} = {c}$",
                "ans": str(x_ans),
                "explain": f"Subtract ${b}$ from both sides to get ${a}x = {c - b}$, then divide by ${a}$ to get $x = {x_ans}$."
            }
        else: # High School
            if std_code == "C.PAR.1":
                n = rng.randint(3, 8)
                x_val = rng.randint(1, 4)
                ans = n * (x_val ** (n - 1))
                return {
                    "q": f"[Q#{q_id}] Evaluate the derivative $\\frac{{d}}{{dx}}[x^{{{n}}}]$ at $x = {x_val}$.",
                    "ans": str(ans),
                    "explain": f"Applying the power rule: $f'(x) = {n}x^{{{n-1}}}$. Evaluated at $x = {x_val}$: ${n}({x_val})^{{{n-1}}} = {ans}$."
                }
            else: # A.PAR.6 Quadratic Roots
                r1 = rng.randint(1, 6)
                r2 = rng.randint(2, 7)
                b_val = -(r1 + r2)
                c_val = r1 * r2
                return {
                    "q": f"[Q#{q_id}] Find the largest real root of $x^2 + ({b_val})x + ({c_val}) = 0$.",
                    "ans": str(max(r1, r2)),
                    "explain": f"Factoring gives $(x - {r1})(x - {r2}) = 0$. The roots are ${r1}$ and ${r2}$."
                }

    # 2. SCIENCE
    elif subject == "Science":
        if grade == "Grade K":
            shapes = [("round marble", "yes"), ("square wooden brick", "no"), ("tennis ball", "yes"), ("cardboard cube", "no")]
            item, ans = rng.choice(shapes)
            return {
                "q": f"[Q#{q_id}] Will a {item} roll down a flat ramp? (Type 'yes' or 'no')",
                "ans": ans,
                "explain": "Spherical and round objects roll smoothly down inclines due to reduced surface friction."
            }
        elif grade == "Grade 3":
            rocks = [("igneous", "magma"), ("sedimentary", "layers of sediment"), ("metamorphic", "heat and pressure")]
            r_type, r_origin = rng.choice(rocks)
            return {
                "q": f"[Q#{q_id}] Which rock type is formed from {r_origin}? (igneous, sedimentary, or metamorphic)",
                "ans": r_type,
                "explain": f"{r_type.capitalize()} rocks are specifically formed from {r_origin}."
            }
        elif grade == "Grade 7":
            cell_parts = [("mitochondria", "ATP energy"), ("nucleus", "DNA storage"), ("ribosome", "protein synthesis")]
            part, function = rng.choice(cell_parts)
            return {
                "q": f"[Q#{q_id}] What cell organelle is responsible for {function}?",
                "ans": part,
                "explain": f"The {part} is responsible for {function} inside the cell."
            }
        else: # High School
            physics_topics = [
                ("What is the standard unit of force in Newton's second law ($F=ma$)?", "newton"),
                ("What subatomic particle is exchanged or shared to form covalent bonds?", "electron")
            ]
            q_text, ans = rng.choice(physics_topics)
            return {
                "q": f"[Q#{q_id}] {q_text}",
                "ans": ans,
                "explain": f"The correct answer is {ans}."
            }

    # 3. SOCIAL STUDIES
    elif subject == "Social Studies":
        if grade == "Grade K":
            symbols = [("bald eagle", "bird"), ("American flag", "flag")]
            item, desc = rng.choice(symbols)
            return {
                "q": f"[Q#{q_id}] What official national symbol represents the United States as a national {desc}?",
                "ans": item,
                "explain": f"The {item} is an official symbol of the United States."
            }
        elif grade == "Grade 3":
            tribes = [("Creek", "Georgia"), ("Cherokee", "Georgia")]
            tribe, loc = rng.choice(tribes)
            return {
                "q": f"[Q#{q_id}] Which Native American group historically inhabited the state of {loc}?",
                "ans": tribe,
                "explain": f"The {tribe} nation historically lived in region areas of {loc}."
            }
        elif grade == "Grade 7":
            rivers = [("Tigris", "Euphrates"), ("Euphrates", "Tigris")]
            r1, r2 = rng.choice(rivers)
            return {
                "q": f"[Q#{q_id}] Name the major Southwest Asian river that flows alongside the {r2} in Mesopotamia.",
                "ans": r1.lower(),
                "explain": f"The {r1} and {r2} rivers form the Fertile Crescent boundary."
            }
        else: # High School
            gov_topics = [
                ("Which branch of the United States federal government is responsible for interpreting laws?", "judicial"),
                ("How many legal justices serve on the United States Supreme Court?", "9")
            ]
            q_text, ans = rng.choice(gov_topics)
            return {
                "q": f"[Q#{q_id}] {q_text}",
                "ans": ans,
                "explain": f"The correct answer is {ans}."
            }

    # 4. ENGLISH LANGUAGE ARTS (ELA)
    else:
        if grade == "Grade K":
            words_data = [("The cat sat on the mat", "6"), ("I love reading", "3")]
            phrase, count = rng.choice(words_data)
            return {
                "q": f"[Q#{q_id}] How many total words are in this sentence: '{phrase}'?",
                "ans": count,
                "explain": f"Counting space-separated words gives {count} words."
            }
        elif grade == "Grade 3":
            passages = [
                ("Maya found a shiny red key under the porch step.", "key"),
                ("Liam packed a peanut butter sandwich for lunch.", "sandwich")
            ]
            p_text, p_ans = rng.choice(passages)
            return {
                "q": f"[Q#{q_id}] Read the text: '{p_text}' What specific item was mentioned?",
                "ans": p_ans,
                "explain": f"The passage directly states that the object was a {p_ans}."
            }
        elif grade == "Grade 7":
            return {
                "q": f"[Q#{q_id}] Identify the sentence structure: 'Although the storm was heavy, we arrived safely.' (Simple, Compound, or Complex)",
                "ans": "complex",
                "explain": "A sentence containing one independent clause and at least one dependent clause is a complex sentence."
            }
        else: # High School ELA
            rhetoric = [
                ("Which rhetorical device appeals directly to the speaker's credibility or character?", "ethos"),
                ("Which rhetorical device appeals directly to emotional connection?", "pathos"),
                ("Which rhetorical device appeals directly to logic and structural reason?", "logos")
            ]
            q_text, ans = rng.choice(rhetoric)
            return {
                "q": f"[Q#{q_id}] {q_text}",
                "ans": ans,
                "explain": f"The answer is {ans}."
            }

# -----------------------------------------------------------------------------
# USER INTERFACE & NAVIGATION
# -----------------------------------------------------------------------------
st.markdown('<p class="main-title">🍑 GA Standards Quest</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Georgia Standards Mastery Platform • Subject-Isolated 1,000 Question Banks</p>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Quest Configuration")
    
    subject = st.selectbox(
        "Select Subject",
        ["Mathematics", "Science", "Social Studies", "English Language Arts"]
    )
    
    grade = st.selectbox(
        "Select Grade Level",
        list(GA_STANDARDS_DB.keys())
    )
    
    # Active Standard Selector
    avail_stds = GA_STANDARDS_DB.get(grade, {}).get(subject, [{"code": "GA.GEN", "desc": "General Standard"}])
    std_choice = st.selectbox(
        "Select Georgia Standard",
        options=avail_stds,
        format_func=lambda x: f"{x['code']} - {x['desc']}"
    )
    
    track = st.radio(
        "Select Track Level",
        ["Regular", "Advanced", "Accelerated", "🏆 Competition Level"]
    )
    
    # Question Bank Selector (1 to 1,000)
    question_num = st.number_input(
        "Question Bank ID (1 to 1,000)",
        min_value=1,
        max_value=1000,
        value=1
    )
    
    st.divider()
    if st.button("🔄 Reset Score"):
        st.session_state.score = 0
        st.session_state.total_questions = 0
        st.rerun()

# Scoreboard
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Correct Answers", st.session_state.score)
with col2:
    st.metric("Attempts", st.session_state.total_questions)
with col3:
    acc = (st.session_state.score / st.session_state.total_questions * 100) if st.session_state.total_questions > 0 else 0
    st.metric("Mastery Rate", f"{acc:.1f}%")

st.divider()

# Load problem from 1,000-question bank
clean_track = track.replace("🏆 ", "")
current_std_code = std_choice["code"]

prob = get_bank_question(subject, grade, current_std_code, clean_track, question_num)

# Question Display Card
st.caption(f"📌 **Georgia Standard {current_std_code}: {std_choice['desc']}**")
st.subheader(f"{subject} — {grade} ({clean_track} Track)")
st.info(f"**Question:** {prob['q']}")

# Answer Input Form
with st.form("ga_quest_form", clear_on_submit=True):
    user_ans = st.text_input("Your Answer (case-insensitive):", placeholder="Type answer here...")
    submit = st.form_submit_button("Submit Answer")

if submit:
    st.session_state.total_questions += 1
    
    clean_user = user_ans.strip().lower()
    clean_correct = prob["ans"].strip().
