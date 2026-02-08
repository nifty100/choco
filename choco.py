import streamlit as st

# Page setup
st.set_page_config(
    page_title="Happy Chocolate Day 🍫",
    layout="centered"
)

# Initialize session state safely
st.session_state.setdefault("accepted", False)
st.session_state.setdefault("unwrapped", False)
st.session_state.setdefault("bites", 0)

TOTAL_BITES = 6

# CSS for graphics
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #5a2e0f;
    margin-bottom: 20px;
}
.text {
    text-align: center;
    font-size: 22px;
    margin-bottom: 15px;
}
.center {
    display: flex;
    justify-content: center;
}
.wrapper {
    width: 260px;
    height: 150px;
    background: linear-gradient(135deg, #d4af7a, #b48b5a);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 6px 12px rgba(0,0,0,0.25);
    font-size: 22px;
    font-weight: bold;
    color: #4b250f;
    text-align: center;
}
.chocolate {
    display: grid;
    grid-template-columns: repeat(3, 65px);
    gap: 8px;
    padding: 15px;
    background: #3b1f0e;
    border-radius: 12px;
}
.block {
    width: 65px;
    height: 55px;
    background: linear-gradient(145deg, #6b3a1e, #4b250f);
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>🍫 Happy Chocolate Day 🍫</div>", unsafe_allow_html=True)

# STEP 1 — Accept chocolate
if not st.session_state.accepted:
    st.markdown("<div class='text'>Will you accept my chocolate?</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes 🍫"):
            st.session_state.accepted = True
            st.rerun()

    with col2:
        if st.button("No 🙈"):
            # Sneaky 😏
            st.session_state.accepted = True
            st.rerun()

# STEP 2 — Branded wrapper
elif not st.session_state.unwrapped:
    st.markdown("<div class='text'>Chocolate accepted 💝</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='center'>
            <div class='wrapper'>
                🍫 Meri Khushki Chocolate 🍫
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🎁 Unwrap Chocolate"):
        st.session_state.unwrapped = True
        st.rerun()

# STEP 3 — Eat chocolate one block at a time
else:
    remaining = TOTAL_BITES - st.session_state.bites

    if remaining > 0:
        st.markdown("<div class='text'>Take a bite 😋</div>", unsafe_allow_html=True)

        blocks_html = "".join("<div class='block'></div>" for _ in range(remaining))

        st.markdown(
            f"""
            <div class='center'>
                <div class='chocolate'>
                    {blocks_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("🍫 Eat one bite"):
            st.session_state.bites += 1
            st.rerun()

        st.progress(st.session_state.bites / TOTAL_BITES)

    else:
        st.balloons()
        st.markdown(
            "<div class='title'>I love you ❤️<br>Bebu 💕</div>",
            unsafe_allow_html=True
        )
