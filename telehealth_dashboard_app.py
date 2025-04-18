import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🩺 Telehealth Operations Dashboard")
st.write("Monitor operational KPIs, trends, and appointments dynamically!")

# Upload the file
uploaded_file = st.file_uploader("Upload Appointment Data CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Show data
    st.subheader("Raw Uploaded Data")
    st.dataframe(df.head())

    # Calculate KPIs
    total_appointments = len(df)
    no_shows = df[df['No_show'] == 1]
    no_show_rate = (len(no_shows) / total_appointments) * 100
    
    st.subheader("📊 KPIs")
    st.metric("Total Appointments", total_appointments)
    st.metric("No-Show Rate (%)", f"{no_show_rate:.2f}%")

    # Line chart: Appointments over months
    if 'Appointment_Month' in df.columns:
        monthly_summary = df.groupby('Appointment_Month').agg({
            'Patient_ID': 'count',
            'No_show': 'sum'
        }).reset_index()

        monthly_summary['No_Show_Rate'] = (monthly_summary['No_show'] / monthly_summary['Patient_ID']) * 100

        st.subheader("📈 Appointments Over Time")
        fig, ax = plt.subplots()
        ax.plot(monthly_summary['Appointment_Month'], monthly_summary['Patient_ID'], marker='o')
        ax.set_xlabel("Month")
        ax.set_ylabel("Number of Appointments")
        ax.set_title("Monthly Appointments Trend")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.subheader("📈 No-Show Rate Over Time")
        fig2, ax2 = plt.subplots()
        ax2.plot(monthly_summary['Appointment_Month'], monthly_summary['No_Show_Rate'], color='red', marker='o')
        ax2.set_xlabel("Month")
        ax2.set_ylabel("No-Show Rate (%)")
        ax2.set_title("Monthly No-Show Rate Trend")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

        # --- Forecast Section ---

st.subheader("🔮 Forecasted Trends")

# Prepare forecast data
forecast_data = {
    "Month": ["April 2022", "May 2022"],
    "Predicted Appointments": [17067, 7267],
    "Predicted No-Show Rate (%)": [49.13, 48.77]
}
forecast_df = pd.DataFrame(forecast_data)

# Display forecast table
st.dataframe(forecast_df.style.format({"Predicted No-Show Rate (%)": "{:.2f}"}))

