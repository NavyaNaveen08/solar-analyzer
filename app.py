import streamlit as st
from PIL import Image
import numpy as np
import os

st.set_page_config(page_title="AI Solar Rooftop Analyzer", layout="wide")

st.title("☀️ AI-Powered Rooftop Solar Potential Analyzer")
st.markdown("Upload a satellite image of a rooftop and get installation recommendations, output estimates, and ROI.")

uploaded_file = st.file_uploader("📤 Upload a rooftop image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("Analyzing rooftop..."):

        width, height = image.size
        total_area_px = width * height

        # Simulated AI output: assume 25% of the rooftop is usable
        usable_ratio = 0.25
        usable_area_m2 = (total_area_px * usable_ratio) / (100 * 100)  # Rough estimate

        # Constants
        efficiency = 0.2  # 200W/m²
        cost_per_watt = 50  # ₹/W
        electricity_rate = 6  # ₹/kWh
        sunlight_hours = 5  # avg/day

        panel_power_kw = usable_area_m2 * 0.2  # kW
        daily_kwh = panel_power_kw * sunlight_hours
        yearly_kwh = daily_kwh * 365

        install_cost = panel_power_kw * 1000 * cost_per_watt
        yearly_savings = yearly_kwh * electricity_rate
        roi_years = install_cost / yearly_savings

    st.success("✅ Analysis Complete!")

    st.subheader("🔍 Rooftop Analysis Report")
    st.write(f"**Usable rooftop area:** {usable_area_m2:.2f} m²")
    st.write(f"**Estimated panel capacity:** {panel_power_kw:.2f} kW")
    st.write(f"**Daily energy output:** {daily_kwh:.2f} kWh")
    st.write(f"**Yearly energy output:** {yearly_kwh:.2f} kWh")
    st.write(f"**Installation cost:** ₹{install_cost:,.0f}")
    st.write(f"**Estimated yearly savings:** ₹{yearly_savings:,.0f}")
    st.write(f"**Return on Investment (ROI):** {roi_years:.1f} years")

    if roi_years < 6:
        st.success("✅ Great investment opportunity!")
    else:
        st.warning("📉 ROI is higher than average.")

    st.markdown("---")
    st.info("💡 *Note: This version uses simulated analysis. Upgrade with real Vision AI for production.*")
