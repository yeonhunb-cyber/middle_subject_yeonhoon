import streamlit as st
import random

# ==============================================================================
# 📢 데이터 재정의
# COMPOUND_DATA: 화학식과 상세 특성 리스트를 모두 포함 (MCQ 출제용)
# ==============================================================================

# EXAMPLES와 ANSWERS는 1번 퀴즈(구성 원소)를 위해 그대로 유지합니다.
EXAMPLES = [
    "물", "포도당", "암모니아", "아세트산", "이산화탄소", "산소",
    "소금", "설탕", "염산", "산화철", "에탄올", "과산화수소",
    "황산", "베이킹소다", "염화칼륨", "질산칼륨", "유리",
    "헬륨", "네온", "불소"
]

ANSWERS = {
    "물": ["H", "O"],
    "포도당": ["C", "H", "O"],
    "암모니아": ["N", "H"],
    "아세트산": ["C", "H", "O"],
    "이산화탄소": ["C", "O"],
    "산소": ["O"],
    "소금": ["Na", "Cl"],
    "설탕": ["C", "H", "O"],
    "염산": ["H", "Cl"],
    "산화철": ["Fe", "O"],
    "에탄올": ["C", "H", "O"],
    "과산화수소": ["H", "O"],
    "황산": ["S", "H", "O"],
    "베이킹소다": ["Na", "H", "C", "O"],
    "염화칼륨": ["K", "Cl"],
    "질산칼륨": ["K", "N", "O"],
    "유리": ["Si", "O"],
    "헬륨": ["He"],
    "네온": ["Ne"],
    "불소": ["F"]
}

# ELEMENTS_POS: (symbol, period, column_index)
ELEMENTS_POS = [
    ("H", 1, 0),   ("He", 1, 7),
    ("Li", 2, 0),  ("Be", 2, 1),  ("B", 2, 2),  ("C", 2, 3),  ("N", 2, 4),  ("O", 2, 5),  ("F", 2, 6),  ("Ne", 2, 7),
    ("Na", 3, 0),  ("Mg", 3, 1),  ("Al", 3, 2), ("Si", 3, 3), ("P", 3, 4),  ("S", 3, 5),  ("Cl", 3, 6), ("Ar", 3, 7),
    ("K", 4, 0),   ("Ca", 4, 1),  ("Fe", 4, 2)
]

# COMPOUND_DATA: 화학식과 상세 특성 리스트를 모두 포함 (MCQ 출제용)
COMPOUND_DATA = {
    "물": {"formula": "H₂O", "props_list": [
        "상온에서 액체 상태이다.",
        "극성 분자로, 많은 물질을 잘 녹인다.",
        "끓는 점이 높고 비열이 커서 온도 변화가 완만하다."
    ]},
    "포도당": {"formula": "C₆H₁₂O₆", "props_list": [
        "생명체의 주요 에너지원이다.",
        "더 이상 분해되지 않는 가장 기본적인 당류이다.",
        "단맛이 나며, 고체 상태로는 설탕처럼 결정 형태로 존재할 수 있다."
    ]},
    "암모니아": {"formula": "NH₃", "props_list": [
        "자극적인 냄새가 나는 기체이다.",
        "물에 잘 녹아 염기성을 띤다.",
        "비료 제조나 냉매로 사용된다."
    ]},
    "아세트산": {"formula": "CH₃COOH", "props_list": [
        "식초의 주요 성분이다(초산).",
        "신맛이 나고 약한 산성을 띤다.",
        "금속과 반응해 수소 기체를 발생시킨다.",
        "‘빙초산’이라고도 불린다."
    ]},
    "이산화탄소": {"formula": "CO₂", "props_list": [
        "무색무취의 기체이다.",
        "광합성의 원료이다.",
        "드라이아이스의 원료로서, 실온에서 기체 상태로 존재한다."
    ]},
    "산소": {"formula": "O₂", "props_list": [
        "무색무취의 기체이다.",
        "연소를 돕지만 스스로 타지는 않는다.",
        "생물의 호흡에 필수적이다."
    ]},
    "소금": {"formula": "NaCl", "props_list": [
        "무색 결정성 고체이다.",
        "물에 잘 녹고, 전해질로 작용한다.",
        "음식의 간을 맞추거나 보존재로 사용된다."
    ]},
    "설탕": {"formula": "C₁₂H₂₂O₁₁", "props_list": [
        "단맛이 나는 흰색 고체이다.",
        "물에 잘 녹지만 전류는 통하지 않는다.",
        "열을 가하면 갈색으로 변한다."
    ]},
    "염산": {"formula": "HCl", "props_list": [
        "무색에 강한 산성 용액이다.",
        "금속과 반응해 수소 기체를 발생시킨다.",
        "위 속의 위산 성분 중 하나이다."
    ]},
    "산화철": {"formula": "Fe₂O₃", "props_list": [
        "붉은색 고체(녹의 주성분)이다.",
        "물에 잘 녹지 않는다.",
        "철이 산소와 반응해 생긴 산화물이다."
    ]},
    "에탄올": {"formula": "C₂H₅OH", "props_list": [
        "무색의 휘발성 액체이다.",
        "특유의 냄새가 있고 물에 잘 섞인다.",
        "소독용이나 연료, 음료 등에 사용된다."
    ]},
    "과산화수소": {"formula": "H₂O₂", "props_list": [
        "무색의 액체로, 불안정하다.",
        "산소를 잘 내놓는 산화제이다.",
        "소독제나 표백제로 쓰인다."
    ]},
    "황산": {"formula": "H₂SO₄", "props_list": [
        "무색의 점성이 큰 액체이다.",
        "강한 산성과 탈수성을 가진다.",
        "비료, 배터리, 화학약품 제조에 쓰인다."
    ]},
    "베이킹소다": {"formula": "NaHCO₃", "props_list": [
        "흰색 가루 형태의 고체이다.",
        "약한 염기성을 띠며 산과 만나면 이산화탄소를 발생시킨다.",
        "제과제빵이나 청소용으로 사용된다."
    ]},
    "염화칼륨": {"formula": "KCl", "props_list": [
        "무색 결정성 고체이다.",
        "물에 잘 녹고 전류를 통하게 한다.",
        "비료나 의료용(수분 보충제)으로 사용된다."
    ]},
    "질산칼륨": {"formula": "KNO₃", "props_list": [
        "무색 결정성 고체이다.",
        "융해성이 높다.",
        "화약이나 비료의 원료이다."
    ]},
    "유리": {"formula": "SiO₂(주성분)", "props_list": [
        "단단하고 투명한 고체이다.",
        "녹는점이 매우 높고 물에 녹지 않는다.",
        "열을 가하면 분자 배열이 달라지며 불투명해진다."
    ]},
    "헬륨": {"formula": "He", "props_list": [
        "무색무취의 기체이다.",
        "공기보다 가볍고 불연성이다.",
        "풍선, 기구, 냉각제 등에 사용된다."
    ]},
    "네온": {"formula": "Ne", "props_list": [
        "무색무취의 기체이다.",
        "전류가 통하면 붉은 빛을 낸다.",
        "네온사인, 광고등에 사용된다."
    ]},
    "불소": {"formula": "F₂", "props_list": [
        "옅은 노란색의 기체이다.",
        "반응성이 매우 높은 할로젠 원소이다.",
        "치약, 불소수, 플루오린화물 제조에 이용된다."
    ]},
}

# ==============================================================================
# 📢 UI 및 페이지 함수
# ==============================================================================

# 물질 특성 정보 표시를 위한 사이드바
def display_sidebar_info(compound_data):
    st.sidebar.title("💧 물질의 주요 특성")
    
    # 현재 페이지 상태 확인
    current_page = st.session_state.get("page", "start")
    
    # 시험(quiz, mcq) 중이거나 최종 결과(final) 페이지에서는 비활성화
    is_disabled = current_page not in ["start", "examples"]
    
    # 선택 박스에 모든 물질의 이름을 리스트로 넣어줍니다.
    selected_material = st.sidebar.selectbox(
        "🔍 확인하고 싶은 물질을 선택하세요", 
        list(compound_data.keys()),
        disabled=is_disabled # 👈 여기서 비활성화 상태를 제어합니다.
    )
    
    if is_disabled:
        st.sidebar.caption("※ 시험 중에는 특성 변경이 불가합니다.")

    # 선택된 물질의 특성 출력
    st.sidebar.subheader(f"🔹 {selected_material}의 주요 특성")
    
    props = compound_data.get(selected_material, {}).get("props_list", [])
    if props:
        for feature in props:
            st.sidebar.write(f"- {feature}")
    else:
        st.sidebar.write("특성 정보가 없습니다.")


# --- 시작 페이지 ---
def start_page():
    # 안내문 출력 (메인 함수에서 이미 출력되므로 주석 처리)
    # st.title("화합물 구성원소 퀴즈") 
    st.write("응시자 정보를 입력하고 시작하세요.")

    # 폼으로 입력을 묶어 제출 시 값이 확실히 저장되도록 함
    with st.form("start_form", clear_on_submit=False):
        # 기존 session_state 값을 기본값으로 넣어 로컬 변수에 저장
        school_val = st.text_input("학교", value=st.session_state.get("school", ""))
        grade_val = st.text_input("학년", value=st.session_state.get("grade", ""))
        class_val = st.text_input("반", value=st.session_state.get("class_room", ""))
        name_val = st.text_input("이름", value=st.session_state.get("student_name", ""))
        
        # ⚠️ 중복 버튼 제거를 위해 st.button 대신 st.form_submit_button 사용
        submitted = st.form_submit_button("시험 시작")

    if submitted:
        # 응시자 정보를 정확히 입력했는지 확인하는 간단한 로직 추가
        if not all([school_val, grade_val, class_val, name_val]):
            st.error("학교, 학년, 반, 이름을 모두 입력해야 시작할 수 있습니다.")
            return

        # 폼에서 받은 값을 명시적으로 session_state에 저장하고 페이지 이동
        st.session_state["school"] = school_val
        st.session_state["grade"] = grade_val
        st.session_state["class_room"] = class_val
        st.session_state["student_name"] = name_val
        st.session_state["page"] = "examples"


# --- 예시 목록 페이지 ---
def examples_page():
    st.header("예시 화합물 / 물질 목록")
    st.write("아래 항목들을 참고하세요 (번호 없음, 4×5 배열):")
    rows = 5
    cols_per_row = 4
    for r in range(rows):
        cols = st.columns(cols_per_row)
        for c in range(cols_per_row):
            idx = r * cols_per_row + c
            if idx < len(EXAMPLES):
                name = EXAMPLES[idx]
                # COMPOUND_DATA에서 화학식 가져오기
                formula = COMPOUND_DATA.get(name, {}).get("formula", "")
                label = f"{name} ({formula})" if formula else name
                cols[c].write(label)
            else:
                cols[c].write("")
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("시험 시작", key="start_exam_btn"):
            # 첫 번째 시험 문제 8문제로 설정
            st.session_state["quiz_items"] = random.sample(EXAMPLES, k=8)
            st.session_state["selections"] = {q: [] for q in st.session_state["quiz_items"]}
            st.session_state["submitted"] = False
            st.session_state["results"] = {}
            st.session_state["page"] = "quiz"
    with col2:
        if st.button("처음으로", key="examples_to_start"):
            st.session_state["page"] = "start"

# --- 1번 퀴즈 페이지 ---
def _nowrap(sym: str) -> str:
    return "\u2060".join(list(sym))

def quiz_page():
    st.header("시험(1/2) — 구성 원소 선택 (주기 배열 수정, 8문제)")
    quiz_items = st.session_state.get("quiz_items", [])
    if not quiz_items:
        st.write("선택된 문제가 없습니다. 예시 페이지에서 시험을 시작하세요.")
        return

    periods = [1, 2, 3, 4]
    # 최대 열 인덱스를 기반으로 열 개수 설정
    max_cols = max(col for (_, _, col) in ELEMENTS_POS) + 1
    indexed_elements = list(enumerate(ELEMENTS_POS, start=1))

    # 퀴즈 문제와 체크박스 출력
    for compound in quiz_items:
        st.subheader(compound)
        safe = "".join(ch if ch.isalnum() else "_" for ch in compound)

        for period in periods:
            cols = st.columns(max_cols)
            for idx, (sym, p, col) in indexed_elements:
                if p != period:
                    continue
                if col < 0 or col >= max_cols:
                    continue
                key = f"chk_{safe}_{idx}"
                label = _nowrap(sym)
                with cols[col]:
                    # st.checkbox는 폼 밖에 있어서 고유 키를 사용해야 함
                    st.checkbox(label, key=key)
        st.write("---")

        # 체크 상태를 session_state에 저장
        selected = []
        for idx, (sym, _, _) in indexed_elements:
            key = f"chk_{safe}_{idx}"
            if st.session_state.get(key, False):
                selected.append(sym)
        st.session_state.setdefault("selections", {})[compound] = selected

    cols = st.columns(4)
    with cols[0]:
        if st.button("제출", key="submit_exam"):
            results = {}
            for compound in quiz_items:
                chosen = set(st.session_state.get("selections", {}).get(compound, []))
                expected = set(ANSWERS.get(compound, []))
                correct = (chosen == expected)
                
                results[compound] = {"chosen": sorted(chosen), "expected": sorted(expected), "correct": correct}
            st.session_state["results"] = results
            st.session_state["submitted"] = True

            # 결과 즉시 출력
            for compound, info in results.items():
                if info["correct"]:
                    st.success(f"✅ {compound} — 정답입니다!")
                    info_data = COMPOUND_DATA.get(compound)
                    if info_data:
                        st.write(f"화학식: {info_data['formula']}")
                else:
                    st.error(f"❌ {compound} — 오답. 선택: {', '.join(info['chosen']) if info['chosen'] else '선택 없음'} | 정답: {', '.join(info['expected']) if info['expected'] else '정답 미등록'}")

    # 다음 페이지 버튼은 제출 후에만 표시
    if st.session_state.get("submitted"):
        # MCQ 문제 준비 로직 업데이트 (COMPOUND_DATA 사용)
        if st.button("다음 페이지 — 특징 맞추기 문제 (5지선다, 8문제)", key="to_mcq"):
            st.session_state["mcq_items"] = random.sample(EXAMPLES, k=8)
            st.session_state["mcq_answers"] = {q: None for q in st.session_state["mcq_items"]}
            
            # 모든 물질의 모든 특성 지문을 하나의 리스트로 통합
            all_props = []
            for info in COMPOUND_DATA.values():
                all_props.extend(info["props_list"]) 

            mcq_options = {}
            for comp in st.session_state["mcq_items"]:
                # 1. 정답 지문은 해당 물질의 props_list 중 하나를 랜덤으로 선택
                correct_props_list = COMPOUND_DATA.get(comp, {}).get("props_list", ["정보 없음"])
                correct_prop = random.choice(correct_props_list) 

                # 2. 오답 지문은 정답 지문과 겹치지 않는 전체 지문 풀에서 선택
                other_props = [p for p in all_props if p != correct_prop]
                
                # 3. 오답 4개 선택 (최대)
                distractors = random.sample(other_props, k=min(4, len(other_props)))
                
                # 4. 정답과 오답을 합쳐 섞음
                opts = distractors + [correct_prop]
                random.shuffle(opts)
                mcq_options[comp] = opts
                
            st.session_state["mcq_options"] = mcq_options
            st.session_state["mcq_submitted"] = False
            st.session_state["page"] = "mcq"

    if st.session_state.get("submitted") and "results" in st.session_state:
        st.write("---")
        st.write("1번 시험 요약:")
        for compound, info in st.session_state["results"].items():
            if info["correct"]:
                st.success(f"{compound}: 정답")
            else:
                st.error(f"{compound}: 오답 (정답: {', '.join(info['expected'])})")

        # 제출 결과 하단에 한 줄짜리 '다음 페이지' 버튼 표시
        st.write("")  # 간격
        if st.button("다음 페이지 — 특징 맞추기 문제 (5지선다, 8문제)", key="to_mcq_after_results"):
            # 이전 버튼과 동일한 MCQ 문제 준비 로직 사용
            st.session_state["mcq_items"] = random.sample(EXAMPLES, k=8)
            st.session_state["mcq_answers"] = {q: None for q in st.session_state["mcq_items"]}
            
            all_props = []
            for info in COMPOUND_DATA.values():
                all_props.extend(info["props_list"]) 

            mcq_options = {}
            for comp in st.session_state["mcq_items"]:
                correct_props_list = COMPOUND_DATA.get(comp, {}).get("props_list", ["정보 없음"])
                correct_prop = random.choice(correct_props_list) 

                other_props = [p for p in all_props if p != correct_prop]
                distractors = random.sample(other_props, k=min(4, len(other_props)))
                opts = distractors + [correct_prop]
                random.shuffle(opts)
                mcq_options[comp] = opts
                
            st.session_state["mcq_options"] = mcq_options
            st.session_state["mcq_submitted"] = False
            st.session_state["page"] = "mcq"


# --- 2번 퀴즈 페이지 (MCQ) ---
def mcq_page():
    st.header("시험(2/2) — 특징 맞추기 (5지선다, 8문제)")
    mcq_items = st.session_state.get("mcq_items", [])
    if not mcq_items:
        st.write("선택된 문제가 없습니다. 이전 페이지에서 시험을 시작하세요.")
        return

    # 옵션을 한 번만 생성/사용하도록 session_state에서 관리 (재렌더 시 순서/내용 고정)
    if "mcq_options" not in st.session_state:
        # 이 페이지에 직접 들어왔을 때 (비정상 경로)를 대비한 안전 장치
        # quiz_page에서 이미 mcq_options가 생성되었기 때문에 보통 실행되지 않음
        
        all_props = []
        for info in COMPOUND_DATA.values():
            all_props.extend(info["props_list"]) 

        mcq_options = {}
        for comp in mcq_items:
            correct_props_list = COMPOUND_DATA.get(comp, {}).get("props_list", ["정보 없음"])
            correct_prop = random.choice(correct_props_list)
            
            other_props = [p for p in all_props if p != correct_prop]
            distractors = random.sample(other_props, k=min(4, len(other_props)))
            opts = distractors + [correct_prop]
            random.shuffle(opts)
            mcq_options[comp] = opts
        st.session_state["mcq_options"] = mcq_options

    # 각 문제 출력: 저장된 옵션 사용, 라디오의 key를 고유하게 설정
    for i, compound in enumerate(mcq_items, start=1):
        # COMPOUND_DATA에서 화학식 가져오기
        formula = COMPOUND_DATA.get(compound, {}).get("formula", "")
        st.subheader(f"{i}. {compound} — {formula}")
        opts = st.session_state["mcq_options"].get(compound, [])
        key = f"mcq_sel_{compound}"
        
        # 라디오 버튼은 선택 시 자동으로 session_state에 저장됨
        st.radio("다음 중 해당 물질의 성질로 옳은 것은?", opts, key=key)
        sel = st.session_state.get(key)
        st.session_state.setdefault("mcq_answers", {})[compound] = sel

    cols = st.columns(3)
    with cols[0]:
        if st.button("제출", key="mcq_submit"):
            results = {}
            correct_count = 0
            for compound in mcq_items:
                chosen = st.session_state.get(f"mcq_sel_{compound}")
                
                # 정답 확인: 선택한 지문이 해당 물질의 props_list 안에 있는지 확인
                correct_props_list = COMPOUND_DATA.get(compound, {}).get("props_list", ["정보 없음"])
                is_correct = (chosen in correct_props_list)
                
                # 결과 표시용 정답 지문: 보기를 만들 때 마지막에 추가한 (섞이기 전) 정답 지문을 가져옴
                # mcq_options[compound]에는 섞인 보기가 들어있으므로, 정답만 따로 찾을 필요가 있음.
                # 여기서는 찾지 않고 그냥 '정답 리스트'라고만 표시하는 것이 논리적입니다.
                
                if is_correct:
                    correct_count += 1
                
                # 결과 저장: 정답 리스트 전체를 보여주기 위해 props_list를 저장
                results[compound] = {
                    "chosen": chosen, 
                    "expected_list": correct_props_list, 
                    "correct": is_correct
                }
                
            st.session_state["mcq_results"] = results
            st.session_state["mcq_submitted"] = True

            st.balloons()
            st.info(f"정답 수: {correct_count}/{len(mcq_items)}")

    # 제출 후 결과 요약과 '결과 보기' 버튼
    if st.session_state.get("mcq_submitted") and "mcq_results" in st.session_state:
        st.write("---")
        st.write("2번 시험 요약:")
        for compound, info in st.session_state["mcq_results"].items():
            # 예상 정답 목록 중 하나를 표시
            expected_str = random.choice(info["expected_list"]) if info["expected_list"] else "정답 정보 없음"
            
            if info["correct"]:
                st.success(f"{compound}: 정답 (선택 지문: {info['chosen']})")
            else:
                st.error(f"{compound}: 오답 (선택: {info['chosen'] or '없음'} | 정답 중 하나: {expected_str})")

        st.write("")
        if st.button("결과 보기 (모든 시험 통합)", key="view_final_results"):
            st.session_state["page"] = "final"

# --- 최종 결과 페이지 ---
def final_page():
    st.header("종합 결과")

    # 응시자 정보 표시
    school = st.session_state.get("school") or "입력 없음"
    grade = st.session_state.get("grade") or "입력 없음"
    class_room = st.session_state.get("class_room") or "입력 없음"
    student_name = st.session_state.get("student_name") or "입력 없음"

    st.subheader("응시자 정보")
    st.write(f"학교: {school}  |  학년: {grade}  |  반: {class_room}  |  이름: {student_name}")

    # 결과 데이터 로드
    quiz_results = st.session_state.get("results", {})
    mcq_results = st.session_state.get("mcq_results", {})
    quiz_total = len(st.session_state.get("quiz_items", []))
    mcq_total = len(st.session_state.get("mcq_items", []))

    # 총정답율 계산 및 평가
    total_questions = quiz_total + mcq_total
    total_correct = (sum(1 for v in quiz_results.values() if v.get("correct")) +
                     sum(1 for v in mcq_results.values() if v.get("correct")))
    pct = (total_correct / total_questions * 100) if total_questions > 0 else 0
    pct_display = round(pct, 1)

    if pct == 100:
        grade_eval = "Perfect 💯"
    elif pct >= 80:
        grade_eval = "Excellent 👍"
    elif pct >= 50:
        grade_eval = "Good 😊"
    else:
        grade_eval = "Try Harder 😥"

    st.subheader("종합 점수")
    st.metric("총 정답률", f"{pct_display}%", f"{total_correct} / {total_questions}")
    st.write(f"**평가**: {grade_eval}")

    # 개별 시험 결과 표시
    st.subheader("1번 시험 결과 (구성 원소)")
    if quiz_total == 0:
        st.write("1번 시험 결과가 없습니다.")
    else:
        quiz_correct = sum(1 for v in quiz_results.values() if v.get("correct"))
        st.write(f"정답 {quiz_correct} / {quiz_total}")
        for comp, info in quiz_results.items():
            if info.get('correct'):
                st.markdown(f"**✅ {comp}**: 정답")
            else:
                st.markdown(f"**❌ {comp}**: 오답 (정답: {', '.join(info.get('expected', []))})")

    st.subheader("2번 시험 결과 (특징 맞추기)")
    if mcq_total == 0:
        st.write("2번 시험 결과가 없습니다.")
    else:
        mcq_correct = sum(1 for v in mcq_results.values() if v.get("correct"))
        st.write(f"정답 {mcq_correct} / {mcq_total}")
        for comp, info in mcq_results.items():
            expected_prop = random.choice(info["expected_list"]) if info["expected_list"] else "정답 정보 없음"
            if info.get('correct'):
                st.markdown(f"**✅ {comp}**: 정답 (선택 지문: {info.get('chosen')})")
            else:
                st.markdown(f"**❌ {comp}**: 오답 (선택: {info.get('chosen') or '없음'} | 정답 중 하나: {expected_prop})")

# ==============================================================================
# 📢 메인 루프 및 초기 설정
# ==============================================================================

# 사이드바에 물질 특성 정보 표시
display_sidebar_info(COMPOUND_DATA)

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "start"
    
    # 안내문 출력 (페이지가 start일 때만 보이게 하는 것이 일반적이지만, 상단에 고정)
    st.title("화합물 구성원소 퀴즈")
    st.markdown(
        """
        ---
        ### 📢 **필독!**

        **1. 응시자 정보 기입 시 주의 사항 (필수)** - 시험 응시 전, 시스템에 본인의 **학년·반·이름**을 정확하게 기재합니다.
        
        **2. 재시험은 불가하므로, 좌측 상단의 물질 특성을 확인한 후 시험에 응시하시기 바랍니다.** - 모든 시험 문제는 물질의 특성 내용에서만 출제 됩니다.

        **3. 시험 결과 최종 제출 방법** 1️⃣ 시험 완료 후 표시되는 점수 확인 화면을 **캡처**합니다.  
        2️⃣ 캡처한 이미지를 **파일로 저장**합니다.  
        3️⃣ 저장된 파일을 **PDF로 변환**합니다.  
        4️⃣ 완성된 PDF 파일을 첨부하여 아래 이메일 주소로 전송합니다.  

        📧 **dusgns1214@naver.com**

        **4. 기타 안내** - 시험 응시 전 궁금한 사항은 미리 문의 바랍니다.

        ---
        """,
        unsafe_allow_html=True
    )
    
    page = st.session_state["page"]
    if page == "start":
        start_page()
    elif page == "examples":
        examples_page()
    elif page == "quiz":
        quiz_page()
    elif page == "mcq":
        mcq_page()
    elif page == "final":
        final_page()
    else:
        st.session_state["page"] = "start"
        start_page()

if __name__ == "__main__":
    main()
