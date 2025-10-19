import streamlit as st
import random

EXAMPLES = [
    "물", "포도당", "암모니아", "아세트산", "이산화탄소", "산소",
    "소금", "설탕", "염산", "산화철", "에탄올", "과산화수소",
    "황산", "베이킹고다", "염화칼륨", "질산칼륨", "유리",
    "헬륨", "네온", "불소"
]

# 원자번호 1~20에 대한 기호, 주기, 족(0-based 그룹 인덱스 0~17)
ELEMENTS_INFO = [
    ("H", 1, 0),   ("He", 1, 17),
    ("Li", 2, 0),  ("Be", 2, 1),  ("B", 2, 12),  ("C", 2, 13),  ("N", 2, 14),  ("O", 2, 15),  ("F", 2, 16),  ("Ne", 2, 17),
    ("Na", 3, 0),  ("Mg", 3, 1),  ("Al", 3, 12), ("Si", 3, 13), ("P", 3, 14),  ("S", 3, 15),  ("Cl", 3, 16), ("Ar", 3, 17),
    ("K", 4, 0),   ("Ca", 4, 1)
]

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
            st.session_state["page"] = "quiz"
    with col2:
        if st.button("처음으로", key="examples_to_start"):
            st.session_state["page"] = "start"

def _nowrap(sym: str) -> str:
    # 문자 사이에 WORD JOINER(U+2060)를 넣어 줄바꿈 방지
    return "\u2060".join(list(sym))

def quiz_page():
    st.header("시험 — 구성 원소 선택 (주기율표 형태, 원자번호 1~20)")
    quiz_items = st.session_state.get("quiz_items", [])
    if not quiz_items:
        st.write("선택된 문제가 없습니다. 처음으로 돌아가세요.")
        if st.button("처음으로", key="quiz_no_items"):
            st.session_state["page"] = "start"
        return

    # 주기 목록
    periods = [1, 2, 3, 4]

    # 각 화합물에 대해 실제 주기별로 원소만 연속 배치 (공백 없음)
    for compound in quiz_items:
        st.subheader(compound)
        safe = "".join(ch if ch.isalnum() else "_" for ch in compound)

        for period in periods:
            # 해당 주기의 원소들(atomic_idx, symbol)
            elems = [(idx, sym) for idx, (sym, p, _) in enumerate(ELEMENTS_INFO, start=1) if p == period]
            if not elems:
                continue
            cols = st.columns(len(elems))
            for col, (idx, sym) in zip(cols, elems):
                key = f"chk_{safe}_{idx}"
                # 기호에 WORD JOINER 삽입해 줄바꿈 방지
                label = _nowrap(sym)
                with col:
                    st.checkbox(label, key=key)

        st.write("---")

        # selections 업데이트
        selected = []
        for idx, (sym, _, _) in enumerate(ELEMENTS_INFO, start=1):
            key = f"chk_{safe}_{idx}"
            if st.session_state.get(key, False):
                selected.append(sym)
        st.session_state.setdefault("selections", {})[compound] = selected

    cols = st.columns(3)
    with cols[0]:
        if st.button("제출", key="submit_exam"):
            st.session_state["submitted"] = True
    with cols[1]:
        if st.button("다시 풀기(재선택)", key="redo_exam"):
            for compound in quiz_items:
                safe = "".join(ch if ch.isalnum() else "_" for ch in compound)
                for idx in range(1, len(ELEMENTS_INFO) + 1):
                    key = f"chk_{safe}_{idx}"
                    st.session_state[key] = False
            st.session_state["selections"] = {q: [] for q in quiz_items}
            st.session_state["submitted"] = False
    with cols[2]:
        if st.button("처음으로", key="quiz_to_start"):
            for compound in st.session_state.get("quiz_items", []):
                safe = "".join(ch if ch.isalnum() else "_" for ch in compound)
                for idx in range(1, len(ELEMENTS_INFO) + 1):
                    key = f"chk_{safe}_{idx}"
                    if key in st.session_state:
                        del st.session_state[key]
            for k in ["quiz_items", "selections", "submitted"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.session_state["page"] = "start"

    if st.session_state.get("submitted"):
        st.success("제출 완료 — 선택한 원소:")
        for compound, sels in st.session_state.get("selections", {}).items():
            st.write(f"- {compound}: {', '.join(sels) if sels else '선택 없음'}")

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
