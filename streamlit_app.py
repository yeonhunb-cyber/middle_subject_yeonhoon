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
                cols[c].write(EXAMPLES[idx])
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
    st.header("시험 1 — 구성 원소 선택 (8문제)")
    quiz_items = st.session_state.get("quiz_items", [])
    if not quiz_items:
        st.write("선택된 문제가 없습니다. 처음으로 돌아가세요.")
        if st.button("처음으로", key="quiz_no_items"):
            st.session_state["page"] = "start"
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
                key = f"chk_{safe}_{idx}"
                label = _nowrap(sym)
                with cols[col]:
                    st.checkbox(label, key=key)
        st.write("---")
        # selections 업데이트
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
            # 피드백
            if all_correct:
                st.success("모두 정답입니다! 🎉")
                try:
                    st.balloons()
                except Exception:
                    pass
            else:
                st.warning("몇 개의 문제가 틀렸습니다. 다음 페이지로 넘어가서 특징 문제를 풀어보세요.")
    with cols[1]:
        if st.button("다시 풀기(재선택)", key="redo_exam"):
            for compound in quiz_items:
                safe = "".join(ch if ch.isalnum() else "_" for ch in compound)
                for idx in range(1, len(ELEMENTS_POS) + 1):
                    key = f"chk_{safe}_{idx}"
                    st.session_state[key] = False
            st.session_state["selections"] = {q: [] for q in quiz_items}
            st.session_state["submitted"] = False
            st.session_state["results"] = {}
    with cols[2]:
        # 다음 페이지로 넘어가는 버튼: 20개 중 랜덤으로 8개 선택하여 특징 문제 준비
        if st.button("다음 페이지 — 특징 문제", key="to_features"):
            st.session_state["feature_items"] = random.sample(EXAMPLES, k=8)
            # prepare options and empty answers
            st.session_state["feature_options"] = {}
            all_props = [info["props"] for info in COMPOUND_INFO.values()]
            for comp in st.session_state["feature_items"]:
                correct = COMPOUND_INFO.get(comp, {}).get("props", "정보 없음")
                distractors = [p for p in all_props if p != correct]
                if len(distractors) >= 4:
                    opts = random.sample(distractors, k=4)
                else:
                    opts = distractors + ["일반적인 무기물", "무색·무취", "정보 없음", "반응성 높음"]
                    opts = opts[:4]
                opts.append(correct)
                random.shuffle(opts)
                st.session_state["feature_options"][comp] = opts
            st.session_state["feature_answers"] = {comp: None for comp in st.session_state["feature_items"]}
            st.session_state["page"] = "features"
    with cols[3]:
        if st.button("처음으로", key="quiz_to_start"):
            for compound in st.session_state.get("quiz_items", []):
                safe = "".join(ch if ch.isalnum() else "_" for ch in compound)
                for idx in range(1, len(ELEMENTS_POS) + 1):
                    key = f"chk_{safe}_{idx}"
                    if key in st.session_state:
                        del st.session_state[key]
            for k in ["quiz_items", "selections", "submitted", "results"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.session_state["page"] = "start"

    if st.session_state.get("submitted") and "results" in st.session_state:
        st.write("요약:")
        for compound, info in st.session_state["results"].items():
            if info["correct"]:
                st.success(f"{compound}: 정답")
            else:
                st.error(f"{compound}: 오답 (정답: {', '.join(info['expected'])})")

def features_page():
    st.header("시험 2 — 특징 맞추기 (5지선다 × 8문제)")
    items = st.session_state.get("feature_items", [])
    if not items:
        st.write("문제가 준비되지 않았습니다. 처음으로 돌아가세요.")
        if st.button("처음으로", key="features_no_items"):
            st.session_state["page"] = "start"
        return

    # 보여주기 및 응답 수집 (radio)
    for i, comp in enumerate(items, start=1):
        st.subheader(f"{i}. {comp}")
        opts = st.session_state["feature_options"].get(comp, [])
        key = f"feat_{comp}"
        # 현재 선택 저장
        prev = st.session_state.get("feature_answers", {}).get(comp)
        choice = st.radio("", opts, index=opts.index(prev) if prev in opts else 0, key=key)
        st.session_state["feature_answers"][comp] = choice

    cols = st.columns(3)
    with cols[0]:
        if st.button("제출", key="submit_features"):
            results = {}
            all_correct = True
            for comp in items:
                chosen = st.session_state.get("feature_answers", {}).get(comp)
                correct = COMPOUND_INFO.get(comp, {}).get("props", "")
                correct_flag = (chosen == correct)
                if not correct_flag:
                    all_correct = False
                results[comp] = {"chosen": chosen, "expected": correct, "correct": correct_flag}
            st.session_state["feature_results"] = results
            st.session_state["feature_submitted"] = True
            if all_correct:
                st.success("모두 정답입니다! 🎉")
                try:
                    st.balloons()
                except Exception:
                    pass
            else:
                st.warning("몇 문제 틀렸습니다. 결과를 확인하세요. ⚠️")
                try:
                    st.snow()
                except Exception:
                    pass
    with cols[1]:
        if st.button("다시 풀기", key="redo_features"):
            st.session_state["feature_answers"] = {comp: None for comp in items}
            st.session_state["feature_submitted"] = False
            if "feature_results" in st.session_state:
                del st.session_state["feature_results"]
    with cols[2]:
        if st.button("처음으로", key="features_to_start"):
            for k in ["feature_items", "feature_options", "feature_answers", "feature_results", "feature_submitted"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.session_state["page"] = "start"

    if st.session_state.get("feature_submitted") and "feature_results" in st.session_state:
        st.write("결과:")
        for comp, info in st.session_state["feature_results"].items():
            if info["correct"]:
                st.success(f"{comp} — 정답")
                info_data = COMPOUND_INFO.get(comp)
                if info_data:
                    st.write(f"화학식: {info_data['formula']}")
                    st.write(f"성질: {info_data['props']}")
            else:
                st.error(f"{comp} — 오답. 선택: {info['chosen'] or '선택 없음'} | 정답: {info['expected']}")

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
    elif page == "features":
        features_page()
    else:
        st.session_state["page"] = "start"
        start_page()

if __name__ == "__main__":
    main()
