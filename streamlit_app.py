import streamlit as st
import random

EXAMPLES = [
    "물", "포도당", "암모니아", "아세트산", "이산화탄소", "산소",
    "소금", "설탕", "염산", "산화철", "에탄올", "과산화수소",
    "황산", "베이킹소다", "염화칼륨", "질산칼륨", "유리",
    "헬륨", "네온", "불소"
]

# ELEMENTS_POS: (symbol, period, column_index)
ELEMENTS_POS = [
    ("H", 1, 0),   ("He", 1, 7),
    ("Li", 2, 0),  ("Be", 2, 1),  ("B", 2, 2),  ("C", 2, 3),  ("N", 2, 4),  ("O", 2, 5),  ("F", 2, 6),  ("Ne", 2, 7),
    ("Na", 3, 0),  ("Mg", 3, 1),  ("Al", 3, 2), ("Si", 3, 3), ("P", 3, 4),  ("S", 3, 5),  ("Cl", 3, 6), ("Ar", 3, 7),
    ("K", 4, 0),   ("Ca", 4, 1),  ("Fe", 4, 2)
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

COMPOUND_INFO = {
    "물": {"formula": "H₂O", "props": "무색·무취의 액체, 좋은 용매"},
    "포도당": {"formula": "C₆H₁₂O₆", "props": "단당류, 에너지원"},
    "암모니아": {"formula": "NH₃", "props": "자극적 냄새, 염기성 기체"},
    "아세트산": {"formula": "CH₃COOH", "props": "산성 액체, 식초의 성분"},
    "이산화탄소": {"formula": "CO₂", "props": "무색 기체, 호흡과 광합성 관련"},
    "산소": {"formula": "O₂", "props": "무색 기체, 연소와 호흡에 필요"},
    "소금": {"formula": "NaCl", "props": "결정성 고체, 식용·보존용"},
    "설탕": {"formula": "C₁₂H₂₂O₁₁", "props": "자당, 단맛이 나는 결정성 고체"},
    "염산": {"formula": "HCl", "props": "강한 산성 용액(염산)"},
    "산화철": {"formula": "Fe₂O₃", "props": "적갈색 고체, 녹의 주성분"},
    "에탄올": {"formula": "C₂H₅OH", "props": "휘발성 액체, 용매·연료·소독제"},
    "과산화수소": {"formula": "H₂O₂", "props": "산화제, 표백·소독에 사용"},
    "황산": {"formula": "H₂SO₄", "props": "강산·탈수제, 산업용"},
    "베이킹소다": {"formula": "NaHCO₃", "props": "약한 염기, 제빵·세정에 사용"},
    "염화칼륨": {"formula": "KCl", "props": "무색·백색 결정, 비료 원료"},
    "질산칼륨": {"formula": "KNO₃", "props": "산화제, 비료와 화약 원료"},
    "유리": {"formula": "SiO₂(주성분)", "props": "비결정질 고체, 투명·단단함"},
    "헬륨": {"formula": "He", "props": "비활성 기체, 가벼움"},
    "네온": {"formula": "Ne", "props": "비활성 기체, 네온사인에 사용"},
    "불소": {"formula": "F₂", "props": "활성할로겐, 매우 반응적 가스"}
}

def start_page():
    st.title("화합물 구성원소 퀴즈")
    st.write("시작 버튼을 눌러 예시 목록 페이지로 이동하세요.")
    if st.button("시작", key="start_btn"):
        st.session_state["page"] = "examples"

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
                formula = COMPOUND_INFO.get(name, {}).get("formula", "")
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

def _nowrap(sym: str) -> str:
    return "\u2060".join(list(sym))

def quiz_page():
    st.header("시험(1/2) — 구성 원소 선택 (주기 배열 수정, 8문제)")
    quiz_items = st.session_state.get("quiz_items", [])
    if not quiz_items:
        st.write("선택된 문제가 없습니다. 예시 페이지에서 시험을 시작하세요.")
        return

    periods = [1, 2, 3, 4]
    max_cols = max(col for (_, _, col) in ELEMENTS_POS) + 1
    indexed_elements = list(enumerate(ELEMENTS_POS, start=1))

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
                    st.checkbox(label, key=key)
        st.write("---")

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
            all_correct = True
            for compound in quiz_items:
                chosen = set(st.session_state.get("selections", {}).get(compound, []))
                expected = set(ANSWERS.get(compound, []))
                correct = (chosen == expected)
                if not correct:
                    all_correct = False
                results[compound] = {"chosen": sorted(chosen), "expected": sorted(expected), "correct": correct}
            st.session_state["results"] = results
            st.session_state["submitted"] = True

            # 결과 즉시 출력 (이팩트 제거)
            for compound, info in results.items():
                if info["correct"]:
                    st.success(f"{compound} — 정답입니다!")
                    info_data = COMPOUND_INFO.get(compound)
                    if info_data:
                        st.write(f"화학식: {info_data['formula']}")
                        st.write(f"성질: {info_data['props']}")
                else:
                    st.error(f"{compound} — 오답. 선택: {', '.join(info['chosen']) if info['chosen'] else '선택 없음'} | 정답: {', '.join(info['expected']) if info['expected'] else '정답 미등록'}")

    # '다시 풀기' 칸은 비워둠
    with cols[1]:
        st.write("")

    # 다음 페이지 버튼은 제출 후에만, 한줄로 표시
    if st.session_state.get("submitted"):
        if st.button("다음 페이지 — 특징 맞추기 문제 (5지선다, 8문제)", key="to_mcq"):
            # MCQ 문제 준비를 session_state에 고정해서 페이지 전환 후 보기가 바뀌지 않도록 함
            st.session_state["mcq_items"] = random.sample(EXAMPLES, k=8)
            st.session_state["mcq_answers"] = {q: None for q in st.session_state["mcq_items"]}
            all_props = [info["props"] for info in COMPOUND_INFO.values()]
            mcq_options = {}
            for comp in st.session_state["mcq_items"]:
                correct_prop = COMPOUND_INFO.get(comp, {}).get("props", "정보 없음")
                other_props = [p for p in all_props if p != correct_prop]
                distractors = random.sample(other_props, k=min(4, len(other_props)))
                opts = distractors + [correct_prop]
                random.shuffle(opts)
                mcq_options[comp] = opts
            st.session_state["mcq_options"] = mcq_options
            st.session_state["mcq_submitted"] = False
            st.session_state["page"] = "mcq"

    # '처음으로' 버튼 삭제 — cols[3] 빈칸으로 유지
    with cols[3]:
        st.write("")

    if st.session_state.get("submitted") and "results" in st.session_state:
        st.write("요약:")
        for compound, info in st.session_state["results"].items():
            if info["correct"]:
                st.success(f"{compound}: 정답")
            else:
                st.error(f"{compound}: 오답 (정답: {', '.join(info['expected'])})")

        # 제출 결과 하단에 한 줄짜리 '다음 페이지' 버튼 표시
        st.write("")  # 간격
        if st.button("다음 페이지 — 특징 맞추기 문제 (5지선다, 8문제)", key="to_mcq_after_results"):
            # MCQ 문제 준비를 session_state에 고정해서 페이지 전환 후 보기가 바뀌지 않도록 함
            st.session_state["mcq_items"] = random.sample(EXAMPLES, k=8)
            st.session_state["mcq_answers"] = {q: None for q in st.session_state["mcq_items"]}
            all_props = [info["props"] for info in COMPOUND_INFO.values()]
            mcq_options = {}
            for comp in st.session_state["mcq_items"]:
                correct_prop = COMPOUND_INFO.get(comp, {}).get("props", "정보 없음")
                other_props = [p for p in all_props if p != correct_prop]
                distractors = random.sample(other_props, k=min(4, len(other_props)))
                opts = distractors + [correct_prop]
                random.shuffle(opts)
                mcq_options[comp] = opts
            st.session_state["mcq_options"] = mcq_options
            st.session_state["mcq_submitted"] = False
            st.session_state["page"] = "mcq"

def mcq_page():
    st.header("시험(2/2) — 특징 맞추기 (5지선다, 8문제)")
    mcq_items = st.session_state.get("mcq_items", [])
    if not mcq_items:
        st.write("선택된 문제가 없습니다. 예시 페이지에서 시험을 시작하세요.")
        return

    # 옵션을 한 번만 생성/사용하도록 session_state에서 관리 (재렌더 시 순서/내용 고정)
    if "mcq_options" not in st.session_state:
        all_props = [info["props"] for info in COMPOUND_INFO.values()]
        mcq_options = {}
        for comp in mcq_items:
            correct_prop = COMPOUND_INFO.get(comp, {}).get("props", "정보 없음")
            other_props = [p for p in all_props if p != correct_prop]
            distractors = random.sample(other_props, k=min(4, len(other_props)))
            opts = distractors + [correct_prop]
            random.shuffle(opts)
            mcq_options[comp] = opts
        st.session_state["mcq_options"] = mcq_options

    # 각 문제 출력: 저장된 옵션 사용, 라디오의 key를 고유하게 설정
    for i, compound in enumerate(mcq_items, start=1):
        formula = COMPOUND_INFO.get(compound, {}).get("formula", "")
        st.subheader(f"{i}. {compound} — {formula}")
        opts = st.session_state["mcq_options"].get(compound, [])
        key = f"mcq_sel_{compound}"
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
                correct_prop = COMPOUND_INFO.get(compound, {}).get("props", "정보 없음")
                is_correct = (chosen == correct_prop)
                if is_correct:
                    correct_count += 1
                results[compound] = {"chosen": chosen, "expected": correct_prop, "correct": is_correct}
            st.session_state["mcq_results"] = results
            st.session_state["mcq_submitted"] = True

            # 제출 후 즉시 축하 이팩트 제거하고 결과 요약만 표시
            st.info(f"정답 수: {correct_count}/{len(mcq_items)}")

    # 제출 후 결과 요약과 '결과 보기' 버튼 (1/2 시험 합산 화면으로 이동)
    if st.session_state.get("mcq_submitted") and "mcq_results" in st.session_state:
        st.write("문제별 결과:")
        for compound, info in st.session_state["mcq_results"].items():
            if info["correct"]:
                st.success(f"{compound}: 정답 — {info['expected']}")
            else:
                st.error(f"{compound}: 오답 — 선택: {info['chosen'] or '없음'} | 정답: {info['expected']}")

        if st.button("결과 보기 (모든 시험 통합)", key="view_final_results"):
            st.session_state["page"] = "final"

def final_page():
    st.header("종합 결과")
    quiz_results = st.session_state.get("results", {})
    mcq_results = st.session_state.get("mcq_results", {})
    quiz_total = len(st.session_state.get("quiz_items", []))
    mcq_total = len(st.session_state.get("mcq_items", []))

    st.subheader("1번 시험 결과")
    if quiz_total == 0:
        st.write("1번 시험 결과가 없습니다.")
    else:
        quiz_correct = sum(1 for v in quiz_results.values() if v.get("correct"))
        st.write(f"정답 {quiz_correct} / {quiz_total}")
        for comp, info in quiz_results.items():
            st.write(f"- {comp}: {'정답' if info.get('correct') else '오답'} (정답: {', '.join(info.get('expected', []))})")

    st.subheader("2번 시험 결과")
    if mcq_total == 0:
        st.write("2번 시험 결과가 없습니다.")
    else:
        mcq_correct = sum(1 for v in mcq_results.values() if v.get("correct"))
        st.write(f"정답 {mcq_correct} / {mcq_total}")
        for comp, info in mcq_results.items():
            st.write(f"- {comp}: {'정답' if info.get('correct') else '오답'} (정답: {info.get('expected')})")

    # 총정답율 계산 및 평가
    total_questions = quiz_total + mcq_total
    total_correct = (sum(1 for v in quiz_results.values() if v.get("correct")) +
                     sum(1 for v in mcq_results.values() if v.get("correct")))
    pct = (total_correct / total_questions * 100) if total_questions > 0 else 0
    pct_display = round(pct, 1)

    if pct == 100:
        grade = "Perfect"
    elif pct >= 80:
        grade = "Excellent"
    elif pct >= 50:
        grade = "Good"
    else:
        grade = "Bad"

    st.subheader("종합 점수")
    st.write(f"총 정답율: {total_correct} / {total_questions} = {pct_display}%")
    st.write(f"평가: {grade}")

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "start"

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
