import streamlit as st
import pandas as pd
import datetime
import pytz
from io import BytesIO

def get_ist_time():
    utc_now = datetime.datetime.utcnow()
    ist = pytz.timezone("Asia/Kolkata")
    return utc_now.replace(tzinfo=pytz.utc).astimezone(ist).strftime("%d-%m-%Y %H:%M:%S")

def load_data():
    if "timesheet_data" not in st.session_state:
        st.session_state.timesheet_data = pd.DataFrame(columns=["Ticket ID", "Task Start Time", "Task End Time", "Team", "Ticket Type", "Activity Type", "Ticket Status"])
    return st.session_state.timesheet_data

def save_data(new_entry):
    st.session_state.timesheet_data = pd.concat([st.session_state.timesheet_data, new_entry], ignore_index=True)

def get_download_link():
    df = load_data()
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output

def main():
    st.title("Timesheet Entry Tool")
    
    if "task_in_progress" not in st.session_state:
        st.session_state.task_in_progress = False
    if "start_time" not in st.session_state:
        st.session_state.start_time = ""
    if "ticket_id" not in st.session_state:
        st.session_state.ticket_id = ""
    if "team" not in st.session_state:
        st.session_state.team = ""
    if "ticket_type" not in st.session_state:
        st.session_state.ticket_type = ""
    if "activity_type" not in st.session_state:
        st.session_state.activity_type = ""
    if "ticket_status" not in st.session_state:
        st.session_state.ticket_status = ""
    if "task_started" not in st.session_state:
        st.session_state.task_started = False
    
    if not st.session_state.task_in_progress:
        st.session_state.ticket_id = st.text_input("Enter Ticket ID:")
        team_options = ["FCC - Triage - Self", "FCC - Second Line Support - Self", "FCC - User Access Support - Self", "MS - All Support - Self", "MS - All - Self", "FCC - Triage - FW US", "FCC - Second Line Support - FW US", "FCC - User Access Support - FW US", "MS - All Support - FW US", "MS - All - Self - FW US", "FCC - Triage - FW IN", "FCC - Second Line Support - FW IN", "FCC - User Access Support - FW IN", "MS - All Support - FW IN", "MS - All - Self - FW IN", "Catalogue", "Snowflake", "Triage", "Perpetua"]
        ticket_type_options = ["Access Requests", "Data Issues", "Other Issues", "Portfolio or catalogue", "Questions", "Task or Change Request", "Triage", "Other Activities"]
        activity_type_options = ["First Response", "Requesting Okta set up", "Sending to Onboarding team", "Sending to Resolver Group", "Net new reports", "Jira ticket raised", "Replicating the data issue", "Closure", "Market Share access", "Follow Up with Requester/Resolver Group", "Interaction with Internal Team", "Providing access", "Checking on Postman", "Interaction with External Team", "Access Provision and Solved", "Sending to DataLake team", "Internal Meeting", "Triage", "Access Removal and Solved", "Sending to Technical Team", "Documentation", "Trainings", "Analyzing/Troubleshooting"]
        ticket_status_options = ["Open", "Pending", "On-Hold", "Solved", "Closed", "New"]
        
        st.session_state.team = st.selectbox("Select Team:", [""] + team_options)
        st.session_state.ticket_type = st.selectbox("Select Ticket Type:", [""] + ticket_type_options)
        st.session_state.activity_type = st.selectbox("Select Activity Type:", [""] + activity_type_options)
        st.session_state.ticket_status = st.selectbox("Select Ticket Status:", [""] + ticket_status_options)
        
        if st.button("Start Task"):
            st.session_state.start_time = get_ist_time()
            st.session_state.task_in_progress = True
            st.session_state.task_started = True
            st.success(f"Task started at {st.session_state.start_time}")
            st.rerun()
    
    if st.session_state.task_started:
        if st.button("End Task"):
            end_time = get_ist_time()
            new_entry = pd.DataFrame({
                "Ticket ID": [st.session_state.ticket_id],
                "Task Start Time": [st.session_state.start_time],
                "Task End Time": [end_time],
                "Team": [st.session_state.team],
                "Ticket Type": [st.session_state.ticket_type],
                "Activity Type": [st.session_state.activity_type],
                "Ticket Status": [st.session_state.ticket_status]
            })
            save_data(new_entry)
            st.success("Entry saved successfully!")
            st.session_state.task_in_progress = False
            st.session_state.task_started = False
            st.session_state.start_time = ""
            st.session_state.ticket_id = ""
            st.session_state.team = ""
            st.session_state.ticket_type = ""
            st.session_state.activity_type = ""
            st.session_state.ticket_status = ""
            st.rerun()
    
    # File Download Option
    st.markdown("### Download Timesheet Data")
    excel_file = get_download_link()
    st.download_button(label="Download Excel File", data=excel_file, file_name="timesheet.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
if __name__ == "__main__":
    main()
