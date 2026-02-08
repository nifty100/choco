import streamlit as st

# Page setup
st.set_page_config(
    page_title="Happy Chocolate Day 🍫",
    layout="centered"
)

# ---------- BACKGROUND MUSIC ----------
st.markdown(
    """
    <iframe width="0" height="0"
    src="https://www.youtube.com/embed/2Vv-BfVoq4g?autoplay=1&loop=1&playlist=2Vv-BfVoq4g"
    frameborder="0"
    allow="autoplay">
    </iframe>
    """,
    unsafe_allow_html=True
)

# Session state
st.session_state.setdefault("accepted", False)
st.session_state.setdefault("unwrapped", False)
st.session_state.setdefault("bites", 0)

TOTAL_BITES = 6

# ---------- CSS ----------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(180deg, #ffd6e8, #ffeaf3);
}

/* Text styles */
.title {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    color: #7a1c3d;
    margin-bottom: 20px;
}
.text {
    text-align: center;
    font-size: 22px;
    color: #5c1a33;
    margin-bottom: 15px;
}
.center {
    display: flex;
    justify-content: center;
}

/* Chocolate wrapper */
.wrapper {
    width: 300px;
    height: 160px;
    background: linear-gradient(135deg, #8b4a2f, #5a2e1a);
    border-radius: 18px;
    box-shadow: 0 10px 22px rgba(0,0,0,0.35);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Foil shine */
.wrapper::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(
        120deg,
        rgba(255,255,255,0.15),
        rgba(255,255,255,0.02),
        rgba(255,255,255,0.15)
    );
    border-radius: 18px;
}

/* Brand band */
.band {
    background: #f6c1d3;
    padding: 14px 20px;
    border-radius: 12px;
    font-size: 22px;
    font-weight: bold;
    color: #6b1e3b;
    text-align: center;
    box-shadow: inset 0 0 8px rgba(0,0,0,0.15);
}

/* Chocolate bar */
.chocolate {
    display: grid;
    grid-template-columns: repeat(3, 70px);
    gap: 10px;
    padding: 18px;
    background: #3b1f0e;
    border-radius: 14px;
    box-shadow: inset 0 0 12px rgba(0,0,0,0.6);
}

.block {
    width: 70px;
    height: 55px;
    background: linear-gradient(145deg, #6b3a1e, #4b250f);
    border-radius: 8px;
    box-shadow: inset 2px 2px 4px rgba(255,255,255,0.15),
                inset -2px -2px 4px rgba(0,0,0,0.4);
}

</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("<div class='title'>🍫 Happy Chocolate Day 🍫</div>", unsafe_allow_html=True)

# ---------- STEP 1: Accept ----------
if not st.session_state.accepted:
    st.markdown("<div class='text'>Will you accept my chocolate?</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes 🍫"):
            st.session_state.accepted = True
            st.rerun()

    with col2:
        if st.button("No 🙈"):
            st.session_state.accepted = True  # sneaky 😏
            st.rerun()

# ---------- STEP 2: Wrapper ----------
elif not st.session_state.unwrapped:
    st.markdown("<div class='text'>Chocolate accepted 💝</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='center'>
            <div class='wrapper'>
                <div class='band'>
                    🍫 Meri Khushki Chocolate 🍫
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🎁 Unwrap Chocolate"):
        st.session_state.unwrapped = True
        st.rerun()

# ---------- STEP 3: Eat ----------
else:
    remaining = TOTAL_BITES - st.session_state.bites

    if remaining > 0:
        st.markdown("<div class='text'>Take one bite 😋</div>", unsafe_allow_html=True)

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
