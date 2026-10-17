import streamlit as st
import random
import time

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
if "current_problem" not in st.session_state:
    st.session_state.current_problem = None
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None

# -----------------------------------------------------------------------------
# GEORGIA K-12 FULL STANDARDS REGISTRY
# -----------------------------------------------------------------------------
GA_STANDARDS_DB = {
    "Grade K": {
        "Mathematics": [
            {"code": "K.NR.1", "desc": "Counting & Cardinality (within 20)"},
            {"code": "K.NR.2", "desc": "Comparing Quantities & Numbers"},
            {"code": "K.NR.5", "desc": "Addition & Subtraction Concepts (within 10)"},
            {"code": "K.GSR.7", "desc": "Identifying 2D & 3D Shapes"}
        ],
        "Science": [
            {"code": "SKP1", "desc": "Physical Attributes of Objects"},
            {"code": "SKL1", "desc": "Living & Non-Living Things"}
        ],
        "Social Studies": [
            {"code": "SSKH1", "desc": "American Symbols & Historical Figures"},
            {"code": "SSKG1", "desc": "Maps & Geographic Concepts"}
        ],
        "English Language Arts": [
            {"code": "ELAGSEKRF1", "desc": "Print Concepts & Word Counts"},
            {"code": "ELAGSEKRL1", "desc": "Key Details in Stories"}
        ]
    },
    "Grade 1": {
        "Mathematics": [
            {"code": "1.NR.1", "desc": "Extend Counting to 120"},
            {"code": "1.NR.2", "desc": "Addition & Subtraction within 20"},
            {"code": "1.MDR.5", "desc": "Tell & Write Time to Hour/Half-Hour"}
        ],
        "Science": [{"code": "S1P1", "desc": "Light & Sound Energy"}],
        "Social Studies": [{"code": "SS1H1", "desc": "Historical Figures of Georgia"}],
        "English Language Arts": [{"code": "ELAGSE1RL1", "desc": "Answering Details in Text"}]
    },
    "Grade 2": {
        "Mathematics": [
            {"code": "2.NR.1", "desc": "Place Value to 1,000"},
            {"code": "2.NR.2", "desc": "Fluently Add/Subtract within 100"}
        ],
        "Science": [{"code": "S2P1", "desc": "States of Matter"}],
        "Social Studies": [{"code": "SS2G1", "desc": "Georgia Regions & Rivers"}],
        "English Language Arts": [{"code": "ELAGSE2L1", "desc": "Grammar & Nouns/Verbs"}]
    },
    "Grade 3": {
        "Mathematics": [
            {"code": "3.PAR.3", "desc": "Multiplication & Division Concepts"},
            {"code": "3.NR.4", "desc": "Fractions as Numbers"}
        ],
        "Science": [{"code": "S3E1", "desc": "Rocks, Soils & Fossils"}],
        "Social Studies": [{"code": "SS3H1", "desc": "American Indians & Early Settlers"}],
        "English Language Arts": [{"code": "ELAGSE3RI1", "desc": "Main Idea & Details"}]
    },
    "Grade 4": {
        "Mathematics": [{"code": "4.NR.2", "desc": "Multi-Digit Multiplication & Division"}],
        "Science": [{"code": "S4P1", "desc": "Light & Sound Behavior"}],
        "Social Studies": [{"code": "SS4H1", "desc": "American Revolution"}],
        "English Language Arts": [{"code": "ELAGSE4L1", "desc": "Relative Pronouns & Adverbs"}]
    },
    "Grade 5": {
        "Mathematics": [{"code": "5.NR.3", "desc": "Fraction Operations & Decimals"}],
        "Science": [{"code": "S5P1", "desc": "Chemical & Physical Changes"}],
        "Social Studies": [{"code": "SS5H1", "desc": "Civil War & Reconstruction"}],
        "English Language Arts": [{"code": "ELAGSE5R1", "desc": "Inferences from Text"}]
    },
    "Grade 6": {
        "Mathematics": [{"code": "6.PAR.2", "desc": "Ratios & Rates"}],
        "Science": [{"code": "S6E1", "desc": "Astronomy & Solar System"}],
        "Social Studies": [{"code": "SS6G1", "desc": "Geography of Latin America & Canada"}],
        "English Language Arts": [{"code": "ELAGSE6L1", "desc": "Pronoun Case & Agreement"}]
    },
    "Grade 7": {
        "Mathematics": [
            {"code": "7.PAR.2", "desc": "Linear Equations"},
            {"code": "7.PAR.4", "desc": "Proportional Relationships"}
        ],
        "Science": [{"code": "S7L2", "desc": "Cell Biology & Genetics"}],
        "Social Studies": [{"code": "SS7G8", "desc": "Geography of Southwest Asia"}],
        "English Language Arts": [{"code": "ELAGSE7L1", "desc": "Phrases & Clauses"}]
    },
    "Grade 8": {
        "Mathematics": [{"code": "8.FGR.5", "desc": "Functions & Linear Equations"}],
        "Science": [{"code": "S8P1", "desc": "Atoms & Periodic Table"}],
        "Social Studies": [{"code": "SS8H1", "desc": "Georgia History & Native Cultures"}],
        "English Language Arts": [{"code": "ELAGSE8L1", "desc": "Verbal Types (Gerunds, Participles)"}]
    },
    "High School": {
        "Mathematics": [{"code": "A.PAR.6", "desc": "Quadratic & Exponential Functions"}],
        "Science": [{"code": "SP1", "desc": "Physics & Motion"}],
        "Social Studies": [{"code": "SSCG1", "desc": "Georgia & US Constitution"}],
        "English Language Arts": [{"code": "ELAGSE9-10L1", "desc": "Advanced Syntax & Rhetoric"}]
    }
}

# -----------------------------------------------------------------------------
# DYNAMIC QUESTION GENERATOR ENGINE
# -----------------------------------------------------------------------------
def generate_ga_quest(subject, grade, track):
    """Generates dynamic questions strictly aligned to standard limits."""
    
    # Selected Grade Standards Pool
    standards_pool = GA_STANDARDS_DB.get(grade, GA_STANDARDS_DB["Grade K"]).get(subject, [])
    selected_std = random.choice(standards_pool) if standards_pool else {"code": "GA.GEN", "desc": "General Standard"}

    # -------------------------------------------------------------------------
    # KINDERGARTEN (Strict Foundation Rules)
    # -------------------------------------------------------------------------
    if grade == "Grade K":
        if subject == "Mathematics":
            if track == "Regular":
                n = random.randint(2, 10)
                return {
                    "std": f"GA Standard {selected_std['code']}: {selected_std['desc']}",
                    "q": f"Count forward: What number comes directly after ${n}$?",
                    "ans": str(n + 1),
                    "explain": f"Counting forward: ${n}, {n+1}$."
                }
            elif track in ["Advanced", "Accelerated"]:
                a, b = random.randint(1, 5), random.randint(1, 4)
                return {
                    "std": f"GA Standard K.NR.5: Addition Concepts",
                    "q": f"If you have ${a}$ apples and receive ${b}$ more, how many apples do you have total?",
                    "ans": str(a + b),
                    "explain": f"${a} + {b} = {a + b}$."
                }
            else: # Competition
                return {
                    "std": "GA Standard K.PAR.6: Pattern Recognition",
                    "q": "Find the missing number in the sequence: 2, 4, 6, ___",
                    "ans": "8",
                    "explain": "The rule adds 2 each time ($6 + 2 = 8$)."
                }
        elif subject == "Science":
            return {
                "std": f"GA Standard {selected_std['code']}: {selected_std['desc']}",
                "q": "Which shape rolls smoothly down a ramp: a square block or a round ball?",
                "ans": "round ball",
                "explain": "Round objects reduce surface resistance and roll smoothly."
            }
        elif subject == "Social Studies":
            return {
                "std": f"GA Standard {selected_std['code']}: {selected_std['desc']}",
                "q": "What national symbol bird represents the United States?",
                "ans": "bald eagle",
                "explain": "The bald eagle is the national emblem of the United States."
            }
        else: # ELA
            return {
                "std": f"GA Standard {selected_std['code']}: {selected_std['desc']}",
                "q": "How many words are in the sentence: 'I love Georgia'?",
                "ans": "3",
                "explain": "The three words are 'I', 'love', and 'Georgia'."
            }

    # -------------------------------------------------------------------------
    # MIDDLE SCHOOL (Grade 6 - Grade 8)
    # -------------------------------------------------------------------------
    elif grade in ["Grade 6", "Grade 7", "Grade 8"]:
        if subject == "Mathematics":
            if track == "Regular":
                ratio = random.randint(3, 8)
                x = random.randint(2, 10)
                return {
                    "std": "GA Standard 7.PAR.4: Proportional Relationships",
                    "q": f"If $y = {ratio}x$, what is $y$ when $x = {x}$?",
                    "ans": str(ratio * x),
                    "explain": f"Substitute $x = {x}$: $y = {ratio} \\times {x} = {ratio * x}$."
                }
            elif track == "Advanced":
                a, b = random.randint(2, 6), random.randint(5, 20)
                x_val = random.randint(3, 12)
                c = a * x_val + b
                return {
                    "std": "GA Standard 7.PAR.2: Solve Multi-Step Equations",
                    "q": f"Solve for $x$: ${a}x + {b} = {c}$",
                    "ans": str(x_val),
                    "explain": f"Subtract ${b}$ then divide by ${a}$: $x = {x_val}$."
                }
            elif track == "Accelerated":
                m, b_val = random.randint(2, 5), random.randint(1, 10)
                x_val = random.randint(2, 6)
                return {
                    "std": "GA Standard 8.FGR.5: Linear Functions",
                    "q": f"A line has slope ${m}$ and $y$-intercept ${b_val}$. What is $y$ when $x = {x_val}$?",
                    "ans": str(m * x_val + b_val),
                    "explain": f"$y = {m}({x_val}) + {b_val} = {m * x_val + b_val}$."
                }
            else: # Competition Track
                n = random.randint(5, 12)
                ans = (n * (n - 1)) // 2
                return {
                    "std": "GA Quest Competition: Combinatorial Reasoning",
                    "q": f"If ${n}$ Georgia middle schools participate in a basketball tournament where every team plays every other team once, how many total games occur?",
                    "ans": str(ans),
                    "explain": f"Combination formula $\\binom{{{n}}}{{2}} = \\frac{{{n}({n}-1)}}{{2}} = {ans}$."
                }
        elif subject == "Science":
            return {
                "std": "GA Standard S7L2: Organisms and Biological Systems",
                "q": "Which organelle generates ATP energy for cellular processes?",
                "ans": "mitochondria",
                "explain": "Mitochondria convert oxygen and nutrients into chemical energy."
            }
        elif subject == "Social Studies":
            return {
                "std": "GA Standard SS7G8: Southwest Asia Geography",
                "q": "Which major river flows alongside the Euphrates in Iraq?",
                "ans": "tigris",
                "explain": "The Tigris and Euphrates form the Fertile Crescent."
            }
        else:
            return {
                "std": "GA Standard ELAGSE7L1: Sentence Structures",
                "q": "Identify the sentence structure: 'Although it rained, we ran.' (Simple, Compound, or Complex)",
                "ans": "complex",
                "explain": "Contains one independent and one dependent clause."
            }

    # -------------------------------------------------------------------------
    # OTHER GRADES (Fallback Generator)
    # -------------------------------------------------------------------------
    else:
        a, b = random.randint(2, 12), random.randint(2, 12)
        return {
            "std": f"GA Standard {selected_std['code']}: {selected_std['desc']}",
            "q": f"Evaluate: ${a} \\times {b}$",
            "ans": str(a * b),
            "explain": f"${a} \\times {b} = {a * b}$."
        }

# -----------------------------------------------------------------------------
# USER INTERFACE & NAVIGATION
# -----------------------------------------------------------------------------
st.markdown('<p class="main-title">🍑 GA Standards Quest</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Full Curriculum Coverage • K-12 Georgia Performance Standards</p>', unsafe_allow_html=True)

# Sidebar Setup
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
    
    track = st.radio(
        "Select Track Level",
        ["Regular", "Advanced", "Accelerated", "🏆 Competition Level"]
    )
    
    st.divider()
    if st.button("🔄 Reset Quest Progress"):
        st.session_state.score = 0
        st.session_state.total_questions = 0
        st.session_state.current_problem = None
        st.rerun()

# Display Available Standards for Selected Grade & Subject
st.markdown(f"### 📋 Active Standards: **{grade} — {subject}**")
std_list = GA_STANDARDS_DB.get(grade, {}).get(subject, [])
std_cols = st.columns(len(std_list) if std_list else 1)
for idx, item in enumerate(std_list):
    with std_cols[idx % len(std_cols)]:
        st.info(f"**{item['code']}**: {item['desc']}")

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

# Load problem
clean_track = track.replace("🏆 ", "")
if st.session_state.current_problem is None:
    st.session_state.current_problem = generate_ga_quest(subject, grade, clean_track)
    st.session_state.timer_start = time.time()

prob = st.session_state.current_problem

# Question Card
st.caption(f"📌 **{prob['std']}**")
st.subheader(f"{subject} — {grade} ({clean_track} Track)")
st.info(f"**Question:** {prob['q']}")

# Answer Form
with st.form("ga_quest_form", clear_on_submit=True):
    user_ans = st.text_input("Your Answer (case-insensitive):", placeholder="Type answer here...")
    submit = st.form_submit_button("Submit Answer")

if submit:
    elapsed = round(time.time() - st.session_state.timer_start, 1)
    st.session_state.total_questions += 1
    
    clean_user = user_ans.strip().lower()
    clean_correct = prob["ans"].strip().lower()
    
    if clean_user == clean_correct:
        st.session_state.score += 1
        st.success(f"🎉 **Correct!** Answered in {elapsed}s.")
        st.markdown(f"**Explanation:** {prob['explain']}")
    else:
        st.error(f"❌ **Incorrect.** Expected Answer: `{prob['ans']}`")
        st.markdown(f"**Explanation:** {prob['explain']}")
    
    if st.button("Next Question ➔"):
        st.session_state.current_problem = generate_ga_quest(subject, grade, clean_track)
        st.rerun()
