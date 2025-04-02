# -*- coding: utf-8 -*-
"""timesheet.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1d-NnM6qzNf5XAFUtud8mQI2DZN37cEvd
"""

import streamlit as st
import pandas as pd
import datetime
import os
import pytz

data_file = "timesheet.xlsx"

def load_data():
    if os.path.exists(data_file):
        return pd.read_excel(data_file)
    return pd.DataFrame(columns=["Ticket ID", "Task Start Time", "Task End Time", "Team", "Ticket Type", "Activity Type", "Ticket Status"])

def save_data(df):
    df.to_excel(data_file, index=False)

def get_ist_time():
    utc_now = datetime.datetime.utcnow()
    ist = pytz.timezone("Asia/Kolkata")
    return utc_now.replace(tzinfo=pytz.utc).astimezone(ist).strftime("%d-%m-%Y %H:%M:%S")

def main():
    st.title("Timesheet Entry Tool")

    ticket_id = st.text_input("Enter Ticket ID:")

    task_start = st.checkbox("Task Start Time")
    task_end = st.checkbox("Task End Time")

    team_options = ["FCC - Triage - Self", "FCC - Second Line Support - Self", "FCC - User Access Support - Self", "MS - All Support - Self", "MS - All - Self", "FCC - Triage - FW US", "FCC - Second Line Support - FW US", "FCC - User Access Support - FW US", "MS - All Support - FW US", "MS - All - Self - FW US", "FCC - Triage - FW IN", "FCC - Second Line Support - FW IN", "FCC - User Access Support - FW IN", "MS - All Support - FW IN", "MS - All - Self - FW IN", "Catalogue", "Snowflake", "Triage", "Perpetua"]
    ticket_type_options = ["Access Requests", "Data Issues", "Other Issues", "Portfolio or catalogue", "Questions", "Task or Change Request", "Triage", "Other Activities"]
    activity_type_options = ["First Response", "Requesting Okta set up", "Sending to Onboarding team", "Sending to Resolver Group", "Net new reports", "Jira ticket raised", "Replicating the data issue", "Closure", "Market Share access", "Follow Up with Requester/Resolver Group", "Interaction with Internal Team", "Providing access", "Checking on Postman", "Interaction with External Team", "Access Provision and Solved", "Sending to DataLake team", "Internal Meeting", "Triage", "Access Removal and Solved", "Sending to Technical Team", "Documentation", "Trainings", "Analyzing/Troubleshooting"]
    ticket_status_options = ["Open", "Pending", "On-Hold", "Solved", "Closed", "New"]

    team = st.selectbox("Select Team:", [""] + team_options)
    ticket_type = st.selectbox("Select Ticket Type:", [""] + ticket_type_options)
    activity_type = st.selectbox("Select Activity Type:", [""] + activity_type_options)
    ticket_status = st.selectbox("Select Ticket Status:", [""] + ticket_status_options)

    if st.button("Submit Entry"):
        df = load_data()

        start_time = get_ist_time() if task_start else ""
        end_time = get_ist_time() if task_end else ""

        new_entry = pd.DataFrame({
            "Ticket ID": [ticket_id],
            "Task Start Time": [start_time],
            "Task End Time": [end_time],
            "Team": [team],
            "Ticket Type": [ticket_type],
            "Activity Type": [activity_type],
            "Ticket Status": [ticket_status]
        })

        df = pd.concat([df, new_entry], ignore_index=True)
        save_data(df)
        st.success("Entry saved successfully!")

if __name__ == "__main__":
    main()