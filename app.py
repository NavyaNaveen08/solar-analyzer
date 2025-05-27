import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

st.set_page_config(layout="wide", page_title="Image Captioning App")

@st.cache_resource
def load_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

processor, model = load_model()

st.title("🖼️ AI-Powered Image Captioning (Free & Offline)")
st.markdown("Upload an image, and the model will describe it!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("Generating caption..."):
        inputs = processor(images=image, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        st.success("✅ Caption Generated!")
        st.markdown(f"**Caption:** {caption}")
