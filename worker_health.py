import streamlit as st
import pandas as pd

def calculate_worker_risk(ppe_compliance, fatigue_level, training_status, near_misses, prev_incidents):
    """
    Evaluates worker risk based on key safety parameters.
    """
    risk_score = 0
    
    # Assess Fatigue Level
    if fatigue_level in ["High", "Critical"]:
        risk_score += 3
    elif fatigue_level == "Moderate":
        risk_score += 1
        
    # Assess PPE Compliance
    if ppe_compliance == "Non-Compliant":
        risk_score += 3
    elif ppe_compliance == "Partial":
        risk_score += 1
        
    # Assess Safety Training
    if training_status in ["Expired", "Pending"]:
        risk_score += 2
        
    # Incidents & Near Misses History
    if near_misses > 2 or prev_incidents > 0:
        risk_score += 2
        
    # Classify overall risk level
    if risk_score >= 6:
        return "Critical", "red"
    elif risk_score >= 4:
        return "High", "orange"
    elif risk_score >= 2:
        return "Medium", "gold"
    else:
        return "Low", "green"


def render_worker_health_page():
    st.title("👷 Worker Health and Safety Monitoring")
    st.markdown("Record, monitor, and assess worker safety metrics and risk factors in real time.")

    # Initialize session storage for demo persistence
    if "worker_data" not in st.session_state:
        st.session_state.worker_data = pd.DataFrame([
            {
                "Worker ID": "W-101",
                "Department": "Extraction",
                "Job Role": "Machine Operator",
                "Shift": "Day",
                "PPE Compliance": "Compliant",
                "Training Status": "Up to Date",
                "Fatigue Level": "Low",
                "Near Misses": 0,
                "Previous Incidents": 0,
                "Risk Level": "Low"
            },
            {
                "Worker ID": "W-102",
                "Department": "Haulage",
                "Job Role": "Truck Driver",
                "Shift": "Night",
                "PPE Compliance": "Non-Compliant",
                "Training Status": "Expired",
                "Fatigue Level": "High",
                "Near Misses": 3,
                "Previous Incidents": 1,
                "Risk Level": "Critical"
            }
        ])

    # Dynamic KPI Summary Metrics
    df = st.session_state.worker_data
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Workers Monitored", len(df))
    col2.metric("PPE Non-Compliance", len(df[df["PPE Compliance"] != "Compliant"]))
    col3.metric("High Fatigue Risk", len(df[df["Fatigue Level"].isin(["High", "Critical"])]))
    col4.metric("High/Critical Risk Workers", len(df[df["Risk Level"].isin(["High", "Critical"])]))

    st.divider()

    # Form to Log/Update Worker Health Status
    with st.expander("➕ Log / Update Worker Safety Record", expanded=True):
        with st.form("worker_health_form", clear_on_submit=True):
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                worker_id = st.text_input("Worker ID", placeholder="e.g. W-103")
                department = st.selectbox("Department", ["Extraction", "Haulage", "Processing", "Maintenance", "Safety"])
                job_role = st.text_input("Job Role", placeholder="e.g. Operator, Technician")
                shift = st.selectbox("Shift", ["Day", "Night"])

            with col_b:
                ppe_compliance = st.selectbox("PPE Compliance", ["Compliant", "Partial", "Non-Compliant"])
                training_status = st.selectbox("Safety Training Status", ["Up to Date", "Pending", "Expired"])
                fatigue_level = st.selectbox("Fatigue Level", ["Low", "Moderate", "High", "Critical"])

            with col_c:
                near_misses = st.number_input("Near Misses (Last 30 Days)", min_value=0, step=1)
                prev_incidents = st.number_input("Previous Incidents", min_value=0, step=1)
                safety_obs = st.text_area("Safety Observations / Notes", placeholder="Note any unsafe conditions observed...")

            submit_btn = st.form_submit_button("Submit Record")

            if submit_btn:
                if not worker_id:
                    st.error("Please provide a valid Worker ID.")
                else:
                    risk_level, color = calculate_worker_risk(
                        ppe_compliance, fatigue_level, training_status, near_misses, prev_incidents
                    )
                    
                    new_entry = {
                        "Worker ID": worker_id,
                        "Department": department,
                        "Job Role": job_role,
                        "Shift": shift,
                        "PPE Compliance": ppe_compliance,
                        "Training Status": training_status,
                        "Fatigue Level": fatigue_level,
                        "Near Misses": near_misses,
                        "Previous Incidents": prev_incidents,
                        "Risk Level": risk_level
                    }
                    
                    st.session_state.worker_data = pd.concat([
                        st.session_state.worker_data, 
                        pd.DataFrame([new_entry])
                    ], ignore_index=True)

                    st.success(f"Record added successfully for {worker_id}!")
                    
                    # Display safety warning popup if risk is high/critical
                    if risk_level in ["High", "Critical"]:
                        st.warning(f"⚠️ **SAFETY ALERT**: Worker {worker_id} flagged as **{risk_level} Risk**! Immediate intervention required.")

    # Data Display & Unsafe Condition Alerts
    st.subheader("📋 Active Worker Safety Roster")
    
    # Filter controls
    filter_dept = st.multiselect("Filter by Department:", options=df["Department"].unique(), default=df["Department"].unique())
    filtered_df = df[df["Department"].isin(filter_dept)]

    st.dataframe(filtered_df, use_container_width=True)

    # Automatically highlight unsafe conditions
    unsafe_workers = filtered_df[filtered_df["Risk Level"].isin(["High", "Critical"])]
    if not unsafe_workers.empty:
        st.subheader("🚨 Unsafe Condition & Alert Summary")
        for idx, row in unsafe_workers.iterrows():
            st.error(
                f"**Worker {row['Worker ID']} ({row['Department']} - {row['Shift']} Shift)** | "
                f"Risk: **{row['Risk Level']}** | PPE: {row['PPE Compliance']} | Fatigue: {row['Fatigue Level']} | "
                f"Training: {row['Training Status']}"
            )