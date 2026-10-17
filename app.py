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
# GEORGIA STANDARDS GENERATOR ENGINE
# -----------------------------------------------------------------------------
def generate_ga_quest(subject, grade, track):
    """Generates questions mapped directly to Georgia Learning Standards."""
    
    # -------------------------------------------------------------------------
    # 1. MATHEMATICS (Georgia K-12 Mathematics Standards)
    # -------------------------------------------------------------------------
    if subject == "Mathematics":
        if "Grade 7" in grade:
            if track == "Regular":
                # Standard: 7.PAR.4 (Proportional Relationships)
                ratio = random.randint(3, 8)
                x = random.randint(2, 10)
                y = ratio * x
                return {
                    "std": "GA Standard 7.PAR.4: Proportional Relationships",
                    "q": f"If $y = {ratio}x$, what is the value of $y$ when $x = {x}$?",
                    "ans": str(y),
                    "explain": f"Substitute $x = {x}$ into the equation: $y = {ratio} \\times {x} = {y}$."
                }
            elif track == "Advanced":
                # Standard: 7.PAR.2 (Expressions & Equations)
                a, b = random.randint(2, 6), random.randint(5, 20)
                x_val = random.randint(3, 12)
                c = a * x_val + b
                return {
                    "std": "GA Standard 7.PAR.2: Solve Multi-Step Equations",
                    "q": f"Solve for $x$: ${a}x + {b} = {c}$",
                    "ans": str(x_val),
                    "explain": f"Subtract ${b}$ from both sides to get ${a}x = {c - b}$, then divide by ${a}$ to get $x = {x_val}$."
                }
            elif track == "Accelerated":
                # Standard: 8.FGR.5 (Linear Functions)
                m, b_val = random.randint(2, 5), random.randint(1, 10)
                x_val = random.randint(2, 6)
                y_val = m * x_val + b_val
                return {
                    "std": "GA Standard 8.FGR.5: Slope-Intercept Form (Accelerated)",
                    "q": f"A line has a slope of ${m}$ and a $y$-intercept of ${b_val}$. What is the value of $y$ when $x = {x_val}$?",
                    "ans": str(y_val),
                    "explain": f"Use $y = mx + b$: $y = {m}({x_val}) + {b_val} = {y_val}$."
                }
            else: # Competition
                # Math Olympiad / AMC 8 style
                n = random.randint(5, 12)
                ans = (n * (n - 1)) // 2
                return {
                    "std": "GA Quest Competition: Combinatorial Reasoning",
                    "q": f"If ${n}$ Georgia middle schools participate in a basketball tournament where every team plays every other team once, how many total games are played?",
                    "ans": str(ans),
                    "explain": f"Use the combination formula $\\binom{{{n}}}{{2}} = \\frac{{{n}({n}-1)}}{{2}} = {ans}$."
                }
        else:
            # General Math Fallback (K-12)
            a, b = random.randint(10, 50), random.randint(2, 10)
            return {
                "std": "GA Standard NR.1: Numeric Reasoning",
                "q": f"Evaluate: ${a} \\times {b}$",
                "ans": str(a * b),
                "explain": f"${a} \\times {b} = {a * b}$"
            }

    # -------------------------------------------------------------------------
    # 2. SCIENCE (Georgia Performance Standards for Science - GSE)
    # -------------------------------------------------------------------------
    elif subject == "Science":
        if "Grade 7" in grade:
            if track in ["Regular", "Advanced"]:
                return {
                    "std": "GA Standard S7L2: Organisms and Biological Systems",
                    "q": "Which organelle is known as the powerhouse of the cell responsible for generating ATP energy?",
                    "ans": "mitochondria",
                    "explain": "The mitochondria convert oxygen and nutrients into chemical energy (ATP) via cellular respiration."
                }
            else:
                return {
                    "std": "GA Standard S7L3: Genetics and Heredity",
                    "q": "If both parents are heterozygous (Tt) for a dominant trait, what percentage chance does an offspring have of displaying the recessive phenotype? (Enter number only)",
                    "ans": "25",
                    "explain": "A Punnett square for Tt × Tt yields TT (25%), Tt (50%), and tt (25%). The recessive phenotype (tt) occurs 25% of the time."
                }
        else:
            return {
                "std": "GA Standard S8P1: Matter and Physical Science",
                "q": "What subatomic particle carries a negative electrical charge?",
                "ans": "electron",
                "explain": "Electrons carry a negative charge, protons carry a positive charge, and neutrons carry no charge."
            }

    # -------------------------------------------------------------------------
    # 3. SOCIAL STUDIES (Georgia Performance Standards for Social Studies)
    # -------------------------------------------------------------------------
    elif subject == "Social Studies":
        if "Grade 7" in grade:
            return {
                "std": "GA Standard SS7G8: Geographic Influence in Southwest Asia",
                "q": "Which major river flows through Iraq and forms part of the historical Mesopotamian Fertile Crescent along with the Euphrates?",
                "ans": "tigris",
                "explain": "The Tigris and Euphrates rivers define the historical region of Mesopotamia."
            }
        elif "Grade 8" in grade:
            return {
                "std": "GA Standard SS8H1: Georgia History & Native Cultures",
                "q": "Which prehistoric Native American culture in Georgia built large earthen mounds and was present when Spanish explorers arrived?",
                "ans": "mississippian",
                "explain": "The Mississippian culture constructed large complex mounds and flourished in Georgia from approximately 800 to 1600 AD."
            }
        else:
            return {
                "std": "GA Standard SSCG1: Georgia Civics & Government",
                "q": "How many branches of government exist under the Georgia State Constitution?",
                "ans": "3",
                "explain": "Georgia's government is divided into Legislative, Executive, and Judicial branches."
            }

    # -------------------------------------------------------------------------
    # 4. ENGLISH LANGUAGE ARTS (ELA)
    # -------------------------------------------------------------------------
    else:
        return {
            "std": "GA Standard ELAGSE7L1: Grammar and Conventions",
            "q": "Identify the type of sentence structure: 'Although it was raining, we went for a run in the park.' (Simple, Compound, Complex, or Compound-Complex)",
            "ans": "complex",
            "explain": "A sentence with one independent clause ('we went for a run in the park') and at least one dependent clause ('Although it was raining') is a complex sentence."
        }

# -----------------------------------------------------------------------------
# USER INTERFACE & NAVIGATION
# -----------------------------------------------------------------------------
st.markdown('<p class="main-title">🍑 GA Standards Quest</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">State-Aligned Practice • Regular, Advanced, Accelerated & Competition Tracks</p>', unsafe_allow_html=True)

# Sidebar Setup
with st.sidebar:
    st.header("⚙️ Quest Configuration")
    
    subject = st.selectbox(
        "Select Subject",
        ["Mathematics", "Science", "Social Studies", "English Language Arts"]
    )
    
    grade = st.selectbox(
        "Select Grade Level",
        ["Grade K", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", 
         "Grade 6", "Grade 7", "Grade 8", "Grade 9 (Alg I / Lit)", "Grade 10 (Geom)", "Grade 11 (Alg II / US Hist)", "Grade 12 (Calc / Econ)"]
    )
    
    track = st.radio(
        "Select Track Level",
        ["Regular", "Advanced", "Accelerated", "🏆 Competition Level"],
        help="Competition track features contest-style reasoning and analytical problems."
    )
    
    st.divider()
    if st.button("🔄 Reset Quest Progress"):
        st.session_state.score = 0
        st.session_state.total_questions = 0
        st.session_state.current_problem = None
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

# Load initial problem
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
