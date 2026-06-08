import random
import streamlit as st
import time

# 1. 페이지 기본 설정 및 테마(CSS) 적용
st.set_page_config(page_title="Hacker Debugging Game", page_icon="💻", layout="centered")

# 배경 테마 및 스타일 설정을 위한 CSS
st.markdown("""
    <style>
    /* 전체 배경색과 글자색 (어두운 개발자 테마) */
    .stApp {
        background-color: #0e1117;
        color: #00FF41; /* 해커 네온 그린 */
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* 시작 버튼 스타일 */
    div.stButton > button:first-child {
        background-color: #00FF41;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        border: none;
    }
    
    /* 입력창 라벨 색상 보정 */
    label {
        color: #00FF41 !important;
    }
    </style>
    """, unsafe_allow_stdio=True)

# 2. 세션 상태 초기화
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.hp = 100
    st.session_state.progress = 0
    st.session_state.turn = 1
    st.session_state.game_over = False
    st.session_state.errors = [
        "❌ NameError: name 'user_id' is not defined",
        "❌ IndexError: list index out of range",
        "❌ ZeroDivisionError: division by zero",
        "❌ IndentationError: unexpected indent",
        "❌ TypeError: can only concatenate str (not 'int') to str",
    ]
    random.shuffle(st.session_state.errors)

# 3. 게임 시작 함수
def start_game():
    st.session_state.started = True

# 4. 수학 문제 생성 함수
def generate_math_problem():
    if not st.session_state.errors:
        st.session_state.game_over = True
        return

    st.session_state.current_error = st.session_state.errors.pop()
    st.session_state.num_math_questions = random.randint(2, 5)
    st.session_state.math_questions = []

    for _ in range(st.session_state.num_math_questions):
        op = random.choice(["+", "-", "*", "/"])
        if op == "+":
            num1, num2 = random.randint(1, 10), random.randint(1, 10)
            ans = num1 + num2
        elif op == "-":
            num1 = random.randint(5, 15)
            num2 = random.randint(1, num1)
            ans = num1 - num2
        elif op == "*":
            num1, num2 = random.randint(2, 9), random.randint(1, 9)
            ans = num1 * num2
        else: # /
            num2 = random.randint(2, 5)
            ans = random.randint(1, 5)
            num1 = num2 * ans
        st.session_state.math_questions.append({"q": f"{num1} {op} {num2}", "a": ans})

# --- 화면 로직 ---

# [화면 1] 시작 화면
if not st.session_state.started:
    st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", caption="System Security Compromised...")
    st.title("🚨 데드라인 1시간 전")
    st.write("당신은 전설적인 해커이자 시니어 개발자입니다.")
    st.write("쏟아지는 버그를 수학 연산 암호로 해결하고 무사히 퇴근하세요.")
    
    if st.button("🚀 미션 시작 (START)"):
        start_game()
        generate_math_problem()
        st.rerun()

# [화면 2] 게임 화면
else:
    # 성공 조건 (폭죽 효과!)
    if st.session_state.progress >= 100:
        st.title("👑 MISSION COMPLETE")
        st.balloons() # 폭죽 효과!
        st.success("🎉 정시 퇴근에 성공했습니다! 당신은 연산의 신입니다!")
        if st.button("다시 도전하기"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
            
    # 실패 조건
    elif st.session_state.hp <= 0:
        st.title("💀 SYSTEM CRASHED")
        st.error("멘탈이 모두 소모되었습니다. 당신은 야근의 늪에 빠졌습니다...")
        if st.button("다시 도전하기"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
            
    # 게임 진행
    else:
        # 상태바 (진행률)
        st.progress(st.session_state.progress / 100)
        
        c1, c2 = st.columns(2)
        c1.write(f"🧠 **MENTAL**: {st.session_state.hp}%")
        c2.write(f"🛠️ **PROGRESS**: {st.session_state.progress}%")
        
        st.write("---")
        st.subheader(f"📟 [버그 {st.session_state.turn}단계]")
        st.code(st.session_state.current_error, language="python")
        
        st.write(f"🔓 암호를 풀기 위해 다음 **{st.session_state.num_math_questions}개**를 계산하세요.")

        with st.form(key="math_form", clear_on_submit=True):
            user_ans = []
            for i, mq in enumerate(st.session_state.math_questions):
                ans = st.number_input(f"Q{i+1}: {mq['q']} =", step=1, key=f"in_{i}")
                user_ans.append(ans)
            
            submit = st.form_submit_button("ENTER (코드 수정)")

        if submit:
            correct_count = 0
            for i, mq in enumerate(st.session_state.math_questions):
                if user_ans[i] == mq['a']:
                    correct_count += 1
            
            if correct_count == st.session_state.num_math_questions:
                st.toast("DEBUG SUCCESS!", icon="✅")
                st.session_state.progress += 25
            else:
                st.toast("COMPILING ERROR...", icon="❌")
                st.session_state.hp -= 20
            
            st.session_state.turn += 1
            generate_math_problem()
            st.rerun()
