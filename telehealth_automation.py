import pandas as pd

# 1. Load the original raw dataset
raw_data = pd.read_csv('telehealth_operations_dataset.csv')

# 2. Cleaning and Transformations

# 2.1 Map Gender: M -> 0, F -> 1
raw_data['Gender'] = raw_data['Gender'].map({'M': 0, 'F': 1})

# 2.2 Map No-show: No -> 0, Yes -> 1
raw_data['No_show'] = raw_data['No_show'].map({'No': 0, 'Yes': 1})

# 2.3 Reminder type: Split into SMS, Email, None 
raw_data['Reminder_SMS'] = (raw_data['Reminder_Method'] == 'SMS').astype(int)
raw_data['Reminder_Email'] = (raw_data['Reminder_Method'] == 'Email').astype(int)
raw_data['Reminder_None'] = (raw_data['Reminder_Method'] == 'None').astype(int)

# 2.4 Follow-up Completed: Map Yes -> 1, No -> 0
raw_data['Follow_Up_Completed'] = raw_data['Follow_Up_Completed'].map({'Yes': 1, 'No': 0})

# 2.5 Follow-Up Sent: Map Yes -> 1, No -> 0
raw_data['Follow_Up_Sent'] = raw_data['Follow_Up_Sent'].map({'Yes': 1, 'No': 0})

# 2.6 Create Appointment Month
raw_data['Appointment_Month'] = pd.to_datetime(raw_data['ScheduledDay']).dt.to_period('M').astype(str)

# 3. Save cleaned data as appointment_data.csv
raw_data.to_csv('appointment_data.csv', index=False)

print("✅ Cleaned appointment_data.csv saved.")

# 4. Create Monthly Aggregates

# Total Appointments per Month
monthly_total = raw_data.groupby('Appointment_Month')['Patient_ID'].count().reset_index()
monthly_total.rename(columns={'Patient_ID': 'Total_Appointments'}, inplace=True)

# No-Show Rate per Month
monthly_noshow = raw_data[raw_data['No_show'] == 1].groupby('Appointment_Month')['Patient_ID'].count().reset_index()
monthly_noshow.rename(columns={'Patient_ID': 'No_Shows'}, inplace=True)

# Merge
monthly_agg = pd.merge(monthly_total, monthly_noshow, on='Appointment_Month', how='left')
monthly_agg['No_Show_Rate'] = monthly_agg['No_Shows'] / monthly_agg['Total_Appointments']
monthly_agg.drop(columns=['No_Shows'], inplace=True)

# 5. Save monthly aggregates
monthly_agg.to_csv('monthly_aggregates.csv', index=False)

print("✅ monthly_aggregates.csv saved.")

print("🎯 Full automation from raw to Tableau-ready files completed!")
