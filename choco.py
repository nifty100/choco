import streamlit as st
import time

# Page setup
st.set_page_config(
    page_title="Happy Chocolate Day 🍫",
    page_icon="🍫",
    layout="centered"
)

# Session state init
if "accepted" not in st.session_state:
    st.session_state.accepted = False

if "unwrapped" not in st.session_state:
    st.session_state.unwrapped = False

if "bites" not in st.session_state:
    st.session_state.bites = 0

# Styling
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    color: #7a3e1d;
}
.choco {
    font-size: 80px;
    text-align: center;
}
.text {
    text-align: center;
    font-size: 22px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>🍫 Happy Chocolate Day 🍫</div>", unsafe_allow_html=True)
st.markdown("<div class='choco'>🍫</div>", unsafe_allow_html=True)

# Step 1: Accept chocolate
if not st.session_state.accepted:
    st.markdown(
        "<div class='text'>Will you accept my chocolate?</div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🍫 Yes"):
            st.session_state.accepted = True
            st.experimental_rerun()

    with col2:
        if st.button("🙈 No"):
            # Evil twist 😏
            st.session_state.accepted = True
            st.experimental_rerun()

# Step 2: Unwrap chocolate
elif not st.session_state.unwrapped:
    st.success("🍫 Chocolate accepted!")
    st.markdown("<div class='text'>Now unwrap the chocolate 😋</div>", unsafe_allow_html=True)

    if st.button("🎁 Unwrap Chocolate"):
        st.session_state.unwrapped = True
        st.experimental_rerun()

# Step 3: Eat chocolate
else:
    st.markdown("<div class='text'>Take a bite 🍫😌</div>", unsafe_allow_html=True)

    if st.session_state.bites < 5:
        if st.button("😋 Eat a bite"):
            st.session_state.bites += 1
            time.sleep(0.3)
            st.experimental_rerun()

        st.progress(st.session_state.bites / 5)

    else:
        st.balloons()
        st.markdown(
            "<div class='title'>I love you ❤️<br>Bebu 💕</div>",
            unsafe_allow_html=True
        )
