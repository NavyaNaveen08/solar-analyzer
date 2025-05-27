import streamlit as st
import openai
import os
import base64

# Set API key from Streamlit secrets
openai.api_key = st.secrets["api_key"]

st.title("☀️ Solar Rooftop Analysis Tool")
st.write("Upload a satellite image of a rooftop to get solar panel recommendations and ROI.")

uploaded_file = st.file_uploader("Upload Satellite Image", type=["jpg", "jpeg", "png"])

def analyze_image(image_bytes):
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": (
                        "You are a solar expert. Analyze this rooftop image and respond in JSON format like:\n"
                        "{'usable_area_m2': ..., 'shaded_area_m2': ..., 'recommended_panels': ..., "
                        "'installation_recommended': 'Yes/No', 'comments': '...'}"
                    )},
                    {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + image_bytes.decode()}}
                ]
            }
        ],
        max_tokens=500
    )
    return response.choices[0].message['content']

def estimate_roi(panels, cost_per_panel=20000, yearly_savings=1500):
    total_cost = panels * cost_per_panel
    savings = panels * yearly_savings
    payback = total_cost / savings if savings > 0 else 0
    return total_cost, savings, round(payback, 1)

if uploaded_file:
    img_bytes = uploaded_file.read()
    img_b64 = base64.b64encode(img_bytes)

    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.write("Analyzing...")

    try:
        result_text = analyze_image(img_b64)
        st.code(result_text)

        result = eval(result_text)

        st.json(result)

        cost, savings, payback = estimate_roi(result['recommended_panels'])

        st.markdown(f"### 💰 ROI Estimates")
        st.markdown(f"- **Cost**: ₹{cost}")
        st.markdown(f"- **Annual Savings**: ₹{savings}")
        st.markdown(f"- **Payback Time**: {payback} years")
    except Exception as e:
        st.error(f"Something went wrong: {e}")
