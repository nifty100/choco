
import streamlit as st

# Page setup
st.set_page_config(
    page_title="Happy Chocolate Day 🍫",
    layout="centered"
)

# Initialize session state
st.session_state.setdefault("accepted", False)
st.session_state.setdefault("unwrapped", False)
st.session_state.setdefault("bites", 0)

TOTAL_BITES = 6  # number of chocolate blocks

# CSS for chocolate graphics
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
.choco-wrapper {
    display: flex;
    justify-content: center;
    margin: 20px 0;
}
.chocolate {
    display: grid;
    grid-template-columns: repeat(3, 60px);
    gap: 6px;
    padding: 15px;
    background: #3b1f0e;
    border-radius: 10px;
}
.block {
    width: 60px;
    height: 50px;
    background: linear-gradient(145deg, #6b3a1e, #4b250f);
    border-radius: 6px;
}
.wrapper {
    width: 220px;
    height: 140px;
    background: linear-gradient(135deg, #c49a6c, #a67c52);
    border-radius: 12px;
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
            # Sneaky logic 😏
            st.session_state.accepted = True
            st.rerun()

# STEP 2 — Wrapped chocolate
elif not st.session_state.unwrapped:
    st.markdown("<div class='text'>Chocolate accepted 💝</div>", unsafe_allow_html=True)
    st.markdown("<div class='choco-wrapper'><div class='wrapper'></div></div>", unsafe_allow_html=True)

    if st.button("🎁 Unwrap Chocolate"):
        st.session_state.unwrapped = True
        st.rerun()

# STEP 3 — Eating chocolate (one bite at a time)
else:
    remaining = TOTAL_BITES - st.session_state.bites

    if remaining > 0:
        st.markdown("<div class='text'>Take a bite 😋</div>", unsafe_allow_html=True)

        blocks_html = "".join("<div class='block'></div>" for _ in range(remaining))

        st.markdown(
            f"""
            <div class='choco-wrapper'>
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
