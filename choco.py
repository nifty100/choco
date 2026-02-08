import streamlit as st

# Page setup
st.set_page_config(page_title="Happy Chocolate Day 🍫", layout="centered")

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("accepted", False)
st.session_state.setdefault("unwrapped", False)
st.session_state.setdefault("bites", 0)
st.session_state.setdefault("muted", False)

TOTAL_BITES = 6

# ---------------- MUSIC EMBED ----------------
mute_val = 1 if st.session_state.muted else 0

st.markdown(
    f"""
    <iframe width="0" height="0"
    src="https://www.youtube.com/embed/2Vv-BfVoq4g?autoplay=1&loop=1&playlist=2Vv-BfVoq4g&mute={mute_val}"
    frameborder="0"
    allow="autoplay">
    </iframe>
    """,
    unsafe_allow_html=True
)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(180deg, #ffd6e8, #ffeaf3);
}

/* Text */
.title {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    color: #7a1c3d;
}
.text {
    text-align: center;
    font-size: 22px;
    color: #5c1a33;
}
.center {
    display: flex;
    justify-content: center;
}

/* Heartbeat */
.heart {
    width: 60px;
    height: 60px;
    background: #ff4d6d;
    position: relative;
    transform: rotate(-45deg);
    animation: beat 1s infinite;
    margin: 15px auto;
}
.heart::before,
.heart::after {
    content: "";
    width: 60px;
    height: 60px;
    background: #ff4d6d;
    border-radius: 50%;
    position: absolute;
}
.heart::before {
    top: -30px;
    left: 0;
}
.heart::after {
    left: 30px;
    top: 0;
}

@keyframes beat {
    0% { transform: scale(1) rotate(-45deg); }
    50% { transform: scale(1.15) rotate(-45deg); }
    100% { transform: scale(1) rotate(-45deg); }
}

/* Wrapper */
.wrapper {
    width: 300px;
    height: 160px;
    background: linear-gradient(135deg, #8b4a2f, #5a2e1a);
    border-radius: 18px;
    box-shadow: 0 10px 22px rgba(0,0,0,0.35);
    display: flex;
    align-items: center;
    justify-content: center;
}
.band {
    background: #f6c1d3;
    padding: 14px 22px;
    border-radius: 12px;
    font-size: 22px;
    font-weight: bold;
    color: #6b1e3b;
}

/* Chocolate */
.chocolate {
    display: grid;
    grid-template-columns: repeat(3, 70px);
    gap: 10px;
    padding: 18px;
    background: #3b1f0e;
    border-radius: 14px;
}
.block {
    width: 70px;
    height: 55px;
    background: linear-gradient(145deg, #6b3a1e, #4b250f);
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<div class='title'>🍫 Happy Chocolate Day 🍫</div>", unsafe_allow_html=True)

# ---------------- MUSIC CONTROL ----------------
col_m1, col_m2, col_m3 = st.columns([1,2,1])
with col_m2:
    if st.button("🔊 Unmute Music" if st.session_state.muted else "🔇 Mute Music"):
        st.session_state.muted = not st.session_state.muted
        st.rerun()

# Heartbeat (visible when music is playing)
if not st.session_state.muted:
    st.markdown("<div class='heart'></div>", unsafe_allow_html=True)

# ---------------- STEP 1 ----------------
if not st.session_state.accepted:
    st.markdown("<div class='text'>Will you accept my chocolate?</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Yes 🍫"):
            st.session_state.accepted = True
            st.rerun()
    with c2:
        if st.button("No 🙈"):
            st.session_state.accepted = True
            st.rerun()

# ---------------- STEP 2 ----------------
elif not st.session_state.unwrapped:
    st.markdown("<div class='text'>Chocolate accepted 💝</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='center'>
            <div class='wrapper'>
                <div class='band'>🍫 Meri Khushki Chocolate 🍫</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🎁 Unwrap Chocolate"):
        st.session_state.unwrapped = True
        st.rerun()

# ---------------- STEP 3 ----------------
else:
    remaining = TOTAL_BITES - st.session_state.bites

    if remaining > 0:
        st.markdown("<div class='text'>Take one bite 😋</div>", unsafe_allow_html=True)

        blocks = "".join("<div class='block'></div>" for _ in range(remaining))
        st.markdown(
            f"<div class='center'><div class='chocolate'>{blocks}</div></div>",
            unsafe_allow_html=True
        )

        if st.button("🍫 Eat one bite"):
            st.session_state.bites += 1
            st.rerun()

        st.progress(st.session_state.bites / TOTAL_BITES)

    else:
        st.balloons()
        st.markdown("<div class='title'>I love you ❤️<br>Bebu 💕</div>", unsafe_allow_html=True)
