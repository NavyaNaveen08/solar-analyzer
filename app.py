import streamlit as st
from PIL import Image
import openai
import io
import base64

# Page Configuration
st.set_page_config(page_title="☀️ Solar Rooftop Analyzer", layout="centered")
st.title("☀️ Solar Rooftop Potential Analyzer")

# File uploader
uploaded_file = st.file_uploader("Upload a satellite image of the rooftop", type=["jpg", "jpeg", "png"])

# API Key input (or use st.secrets if deploying)
api_key = st.text_input("Enter your OpenAI API key", type="password")

# Set API key if provided
if api_key:
    openai.api_key = api_key

def analyze_image(image_bytes):
    # Encode image to base64 if needed
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # Simulated response — replace with real OpenAI Vision call if needed
    prompt = (
        "Analyze the solar potential of the rooftop in this image. "
        "Provide installation suitability, usable area estimate, and ROI projection."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error during analysis:\n\n{e}"

# Handle image and trigger analysis
if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("🔍 Analyze Solar Potential"):
        with st.spinner("Analyzing image..."):
            result = analyze_image(uploaded_file.read())
            st.markdown("### 🧠 Analysis Result")
            st.success(result)
