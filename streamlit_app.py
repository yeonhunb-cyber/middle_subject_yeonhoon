import streamlit as st
import random

EXAMPLES = [
    "물", "포도당", "암모니아", "아세트산", "이산화탄소", "산소",
    "소금", "설탕", "염산", "산화철", "에탄올", "과산화수소",
    "황산", "베이킹소다", "염화칼륨", "질산칼륨", "유리",
    "헬륨", "네온", "불소"
]

# ELEMENTS_ORDERED: (symbol, period)
ELEMENTS_ORDERED = [
    ("H", 1), ("He", 1),
    ("Li", 2), ("Be", 2), ("B", 2), ("C", 2), ("N", 2), ("O", 2), ("F", 2), ("Ne", 2),
    ("Na", 3), ("Mg", 3), ("Al", 3), ("Si", 3), ("P", 3), ("S", 3), ("Cl", 3), ("Ar", 3),
    ("K", 4), ("Ca", 4), ("Fe", 4)
]

# 정답 매핑
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

# 화학식 및 간단한 성질 정보
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
            st.session_state["quiz_items"] = random.sample(EXAMPLES, k=3)
            st.session_state["selections"] = {q: [] for q in st.session_state["quiz_items"]}
            st.session_state["submitted"] = False
            st.session_state["results"] = {}
            st.session_state["page"] = "quiz"
    with col2:
        if st.button("처음으로", key="examples_to_start"):
            st.session_state["page"] = "start"

def _nowrap(sym: str) -> str:
    # 문자 사이에 WORD JOINER(U+2060)를 넣어 줄바꿈 방지
    return "\u2060".join(list(sym))

def quiz_page():
    st.header("시험 — 구성 원소 선택 (주기별 연속 배치)")
    quiz_items = st.session_state.get("quiz_items", [])
    if not quiz_items:
        st.write("선택된 문제가 없습니다. 처음으로 돌아가세요.")
        if st.button("처음으로", key="quiz_no_items"):
            st.session_state["page"] = "start"
        return

    periods = [1, 2, 3, 4]

    for compound in quiz_items:
        st.subheader(compound)
        safe = "".join(ch if ch.isalnum() else "_" for ch in compound)

        # 각 주기(period)마다 그 주기에 속한 원소만 연속 배열 (공백 없음)
        for period in periods:
            elems = [(idx, sym) for idx, (sym, p) in enumerate(ELEMENTS_ORDERED, start=1) if p == period]
            if not elems:
                continue
            cols = st.columns(len(elems))
            for col, (idx, sym) in zip(cols, elems):
                key = f"chk_{safe}_{idx}"
                label = _nowrap(sym)
                with col:
                    st.checkbox(label, key=key)

        st.write("---")

        # selections 업데이트
        selected = []
        for idx, (sym, _) in enumerate(ELEMENTS_ORDERED, start=1):
            key = f"chk_{safe}_{idx}"
            if st.session_state.get(key, False):
                selected.append(sym)
        st.session_state.setdefault("selections", {})[compound] = selected

    cols = st.columns(3)
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

            # 개별 결과와 추가 정보 표시
            for compound, info in results.items():
                if info["correct"]:
                    st.success(f"{compound} — 정답입니다! 🎉")
                    info_data = COMPOUND_INFO.get(compound)
                    if info_data:
                        st.write(f"화학식: {info_data['formula']}")
                        st.write(f"성질: {info_data['props']}")
                    try:
                        st.balloons()
                    except Exception:
                        pass
                else:
                    st.error(f"{compound} — 오답. 선택: {', '.join(info['chosen']) if info['chosen'] else '선택 없음'} | 정답: {', '.join(info['expected']) if info['expected'] else '정답 미등록'}")
            # 전체 세레머니
            if all_correct:
                try:
                    st.balloons()
                except Exception:
                    pass
            else:
                try:
                    st.snow()
                except Exception:
                    pass
    with cols[1]:
        if st.button("다시 풀기(재선택)", key="redo_exam"):
            for compound in quiz_items:
                safe = "".join(ch if ch.isalnum() else "_" for ch in compound)
                for idx in range(1, len(ELEMENTS_ORDERED) + 1):
                    key = f"chk_{safe}_{idx}"
                    st.session_state[key] = False
            st.session_state["selections"] = {q: [] for q in quiz_items}
            st.session_state["submitted"] = False
            st.session_state["results"] = {}
    with cols[2]:
        if st.button("처음으로", key="quiz_to_start"):
            for compound in st.session_state.get("quiz_items", []):
                safe = "".join(ch if ch.isalnum() else "_" for ch in compound)
                for idx in range(1, len(ELEMENTS_ORDERED) + 1):
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

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "start"

    if st.session_state["page"] == "start":
        start_page()
    elif st.session_state["page"] == "examples":
        examples_page()
    elif st.session_state["page"] == "quiz":
        quiz_page()
    else:
        st.session_state["page"] = "start"
        start_page()

if __name__ == "__main__":
    main()
