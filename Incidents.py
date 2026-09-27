import streamlit as st
import pandas as pd


def render_incidents_page():

    st.title("🚨 Safety Incident Management")

    st.write(
        "Record, monitor and analyse safety incidents occurring within the mine."
    )

    # ==========================================================
    # 1. INITIALISE INCIDENT DATA
    # ==========================================================

    if "incident_data" not in st.session_state:

        st.session_state.incident_data = pd.DataFrame([
            {
                "Incident ID": "INC-001",
                "Date": "2026-09-20",
                "Time": "08:30",
                "Shift": "Day",
                "Location": "Extraction Area",
                "Department": "Mining",
                "Incident Type": "Near Miss",
                "Severity": "Medium",
                "Injury": "No",
                "LTI": "No",
                "Cause": "Unsafe condition",
                "Corrective Action": "Area inspected and hazard removed",
                "Status": "Closed"
            }
        ])

    # ==========================================================
    # 2. GET CURRENT INCIDENT DATA
    # ==========================================================

    df = st.session_state.incident_data

    # ==========================================================
    # 3. KPI SUMMARY
    # ==========================================================

    st.subheader("📊 Incident Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Incidents",
        len(df)
    )

    col2.metric(
        "Near Misses",
        len(df[df["Incident Type"] == "Near Miss"])
    )

    col3.metric(
        "Injuries",
        len(df[df["Injury"] == "Yes"])
    )

    col4.metric(
        "LTI Cases",
        len(df[df["LTI"] == "Yes"])
    )

    st.divider()

    # ==========================================================
    # 4. RECORD NEW INCIDENT
    # ==========================================================

    with st.expander(
        "➕ Record New Safety Incident",
        expanded=True
    ):

        with st.form(
            "incident_form",
            clear_on_submit=True
        ):

            col1, col2, col3 = st.columns(3)

            # --------------------------------------------------
            # COLUMN 1
            # --------------------------------------------------

            with col1:

                incident_id = st.text_input(
                    "Incident ID",
                    placeholder="e.g. INC-002"
                )

                incident_date = st.date_input(
                    "Date"
                )

                incident_time = st.time_input(
                    "Time"
                )

                shift = st.selectbox(
                    "Shift",
                    [
                        "Day",
                        "Night"
                    ]
                )

                location = st.text_input(
                    "Location",
                    placeholder="e.g. Underground Section A"
                )

            # --------------------------------------------------
            # COLUMN 2
            # --------------------------------------------------

            with col2:

                department = st.selectbox(
                    "Department",
                    [
                        "Mining",
                        "Engineering",
                        "Maintenance",
                        "Processing",
                        "Safety"
                    ]
                )

                incident_type = st.selectbox(
                    "Incident Type",
                    [
                        "Near Miss",
                        "Injury",
                        "Equipment Incident",
                        "Environmental Incident",
                        "Unsafe Condition",
                        "Other"
                    ]
                )

                severity = st.selectbox(
                    "Severity",
                    [
                        "Low",
                        "Medium",
                        "High",
                        "Critical"
                    ]
                )

                injury = st.selectbox(
                    "Injury Occurred?",
                    [
                        "No",
                        "Yes"
                    ]
                )

                lti = st.selectbox(
                    "Lost Time Injury (LTI)?",
                    [
                        "No",
                        "Yes"
                    ]
                )

            # --------------------------------------------------
            # COLUMN 3
            # --------------------------------------------------

            with col3:

                cause = st.text_area(
                    "Cause",
                    placeholder="Describe the cause of the incident..."
                )

                corrective_action = st.text_area(
                    "Corrective Action",
                    placeholder="Describe the corrective action taken..."
                )

                status = st.selectbox(
                    "Status",
                    [
                        "Open",
                        "Under Investigation",
                        "Corrective Action",
                        "Closed"
                    ]
                )

            # --------------------------------------------------
            # SUBMIT BUTTON
            # --------------------------------------------------

            submit_incident = st.form_submit_button(
                "Submit Incident"
            )

            # ==================================================
            # 5. VALIDATE AND SAVE INCIDENT
            # ==================================================

            if submit_incident:

                if incident_id == "":
                    st.error(
                        "Please provide an Incident ID."
                    )

                elif location == "":
                    st.error(
                        "Please provide the incident location."
                    )

                else:

                    new_incident = {
                        "Incident ID": incident_id,
                        "Date": str(incident_date),
                        "Time": str(incident_time),
                        "Shift": shift,
                        "Location": location,
                        "Department": department,
                        "Incident Type": incident_type,
                        "Severity": severity,
                        "Injury": injury,
                        "LTI": lti,
                        "Cause": cause,
                        "Corrective Action": corrective_action,
                        "Status": status
                    }

                    st.session_state.incident_data = pd.concat(
                        [
                            st.session_state.incident_data,
                            pd.DataFrame([new_incident])
                        ],
                        ignore_index=True
                    )

                    st.success(
                        f"Incident {incident_id} recorded successfully."
                    )

                    # ==================================================
                    # 6. SAFETY ALERT FOR HIGH/CRITICAL INCIDENTS
                    # ==================================================

                    if severity in [
                        "High",
                        "Critical"
                    ]:

                        st.warning(
                            f"⚠️ SAFETY ALERT: Incident "
                            f"{incident_id} has been classified as "
                            f"{severity} severity."
                        )

    # ==========================================================
    # 7. INCIDENT RECORDS
    # ==========================================================

    st.subheader("📋 Incident Records")

    st.dataframe(
        st.session_state.incident_data,
        use_container_width=True
    )

    # ==========================================================
    # 8. FILTER INCIDENTS
    # ==========================================================

    st.subheader("🔎 Filter Incidents")

    filter_department = st.multiselect(
        "Department",
        options=st.session_state.incident_data[
            "Department"
        ].unique(),
        default=st.session_state.incident_data[
            "Department"
        ].unique()
    )

    filtered_incidents = st.session_state.incident_data[
        st.session_state.incident_data[
            "Department"
        ].isin(filter_department)
    ]

    st.dataframe(
        filtered_incidents,
        use_container_width=True
    )

    # ==========================================================
    # 9. HIGH AND CRITICAL INCIDENT ALERTS
    # ==========================================================

    high_risk_incidents = filtered_incidents[
        filtered_incidents["Severity"].isin(
            [
                "High",
                "Critical"
            ]
        )
    ]

    if not high_risk_incidents.empty:

        st.subheader(
            "🚨 High and Critical Incident Alerts"
        )

        for _, row in high_risk_incidents.iterrows():

            st.error(
                f"Incident **{row['Incident ID']}** | "
                f"Severity: **{row['Severity']}** | "
                f"Department: {row['Department']} | "
                f"Location: {row['Location']} | "
                f"Status: {row['Status']}"
            )
