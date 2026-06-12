import streamlit as st

st.set_page_config(page_title="Fashion AI", layout="centered")

st.title("✨ Fashion AI Assistant")

uploaded_file = st.file_uploader(
    "Upload your outfit image 👗",
    type=["jpg", "jpeg", "png"]
)

style = st.selectbox(
    "Choose Style",
    [
        "Outfit Analysis",
        "Accessories Match",
        "Wedding Look",
        "Streetwear Critique"
    ]
)

if uploaded_file:

    st.image(uploaded_file, width=300)

    if st.button("Analyze Outfit ✨"):

        st.write("AI response will come here...")