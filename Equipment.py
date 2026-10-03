import streamlit as st
import pandas as pd


# ---------------------------------------------------------
# EQUIPMENT CONDITION FUNCTIONS
# ---------------------------------------------------------

def get_temperature_status(temperature):
    if temperature < 80:
        return "Normal"
    elif temperature <= 100:
        return "Warning"
    else:
        return "Critical"


def get_vibration_status(vibration):
    if vibration < 5:
        return "Normal"
    elif vibration <= 8:
        return "Warning"
    else:
        return "Critical"


def get_condition_status(temperature, vibration):
    temp_status = get_temperature_status(temperature)
    vibration_status = get_vibration_status(vibration)

    if "Critical" in [temp_status, vibration_status]:
        return "Critical"
    elif "Warning" in [temp_status, vibration_status]:
        return "Warning"
    else:
        return "Normal"


def calculate_availability(operating_hours, downtime):
    total_time = operating_hours + downtime

    if total_time == 0:
        return 0

    return (operating_hours / total_time) * 100


# ---------------------------------------------------------
# MAIN EQUIPMENT PAGE
# ---------------------------------------------------------

def render_equipment_page():

    st.title("⚙️ Equipment Condition Monitoring")

    st.write(
        "Monitor equipment operating conditions, maintenance status, "
        "downtime and availability."
    )

    st.info(
        "Note: The temperature and vibration values used in this prototype "
        "are educational monitoring thresholds and are not manufacturer "
        "or mine-specific safety limits."
    )

    # -----------------------------------------------------
    # SAMPLE EQUIPMENT DATA
    # -----------------------------------------------------

    if "equipment_data" not in st.session_state:

        st.session_state.equipment_data = pd.DataFrame([
            {
                "Equipment ID": "EQ-001",
                "Equipment Type": "Haul Truck",
                "Manufacturer": "Caterpillar",
                "Operating Hours": 1800,
                "Temperature": 75.0,
                "Vibration": 4.2,
                "Fuel Level": 78,
                "Brake Status": "Good",
                "Tyre Status": "Good",
                "Engine Status": "Good",
                "Maintenance Status": "Up to Date",
                "Downtime": 120,
                "Availability": 93.75,
                "Condition": "Normal"
            },
            {
                "Equipment ID": "EQ-002",
                "Equipment Type": "Excavator",
                "Manufacturer": "Komatsu",
                "Operating Hours": 2200,
                "Temperature": 92.0,
                "Vibration": 6.5,
                "Fuel Level": 45,
                "Brake Status": "Good",
                "Tyre Status": "Good",
                "Engine Status": "Warning",
                "Maintenance Status": "Due",
                "Downtime": 300,
                "Availability": 88.0,
                "Condition": "Warning"
            }
        ])

    # -----------------------------------------------------
    # ADD EQUIPMENT
    # -----------------------------------------------------

    with st.expander("➕ Add Equipment Record", expanded=True):

        with st.form("equipment_form"):

            col1, col2, col3 = st.columns(3)

            with col1:

                equipment_id = st.text_input(
                    "Equipment ID",
                    placeholder="e.g. EQ-003"
                )

                equipment_type = st.selectbox(
                    "Equipment Type",
                    [
                        "Haul Truck",
                        "Excavator",
                        "Drill Rig",
                        "Loader",
                        "Dozer",
                        "Grader",
                        "Other"
                    ]
                )

                manufacturer = st.text_input(
                    "Manufacturer",
                    placeholder="e.g. Caterpillar"
                )

                operating_hours = st.number_input(
                    "Operating Hours",
                    min_value=0.0,
                    step=1.0
                )

            with col2:

                temperature = st.number_input(
                    "Temperature (°C)",
                    min_value=0.0,
                    step=0.1
                )

                vibration = st.number_input(
                    "Vibration",
                    min_value=0.0,
                    step=0.1
                )

                fuel_level = st.number_input(
                    "Fuel Level (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=1.0
                )

                brake_status = st.selectbox(
                    "Brake Status",
                    ["Good", "Warning", "Fault"]
                )

            with col3:

                tyre_status = st.selectbox(
                    "Tyre Status",
                    ["Good", "Warning", "Fault"]
                )

                engine_status = st.selectbox(
                    "Engine Status",
                    ["Good", "Warning", "Fault"]
                )

                maintenance_status = st.selectbox(
                    "Maintenance Status",
                    [
                        "Up to Date",
                        "Due",
                        "Overdue",
                        "Under Maintenance"
                    ]
                )

                downtime = st.number_input(
                    "Downtime (hours)",
                    min_value=0.0,
                    step=1.0
                )

            submit_equipment = st.form_submit_button(
                "Add Equipment"
            )

            if submit_equipment:

                if equipment_id == "":
                    st.error("Please enter an Equipment ID.")

                elif manufacturer == "":
                    st.error("Please enter the manufacturer.")

                else:

                    availability = calculate_availability(
                        operating_hours,
                        downtime
                    )

                    condition = get_condition_status(
                        temperature,
                        vibration
                    )

                    new_equipment = {
                        "Equipment ID": equipment_id,
                        "Equipment Type": equipment_type,
                        "Manufacturer": manufacturer,
                        "Operating Hours": operating_hours,
                        "Temperature": temperature,
                        "Vibration": vibration,
                        "Fuel Level": fuel_level,
                        "Brake Status": brake_status,
                        "Tyre Status": tyre_status,
                        "Engine Status": engine_status,
                        "Maintenance Status": maintenance_status,
                        "Downtime": downtime,
                        "Availability": availability,
                        "Condition": condition
                    }

                    st.session_state.equipment_data = pd.concat(
                        [
                            st.session_state.equipment_data,
                            pd.DataFrame([new_equipment])
                        ],
                        ignore_index=True
                    )

                    st.success(
                        f"Equipment {equipment_id} added successfully."
                    )

                    if condition == "Critical":
                        st.error(
                            f"🚨 Equipment {equipment_id} has a "
                            f"CRITICAL condition."
                        )

                    elif condition == "Warning":
                        st.warning(
                            f"⚠️ Equipment {equipment_id} requires attention."
                        )

    # -----------------------------------------------------
    # REFRESH DATA
    # -----------------------------------------------------

    df = st.session_state.equipment_data

    # -----------------------------------------------------
    # DASHBOARD KPIs
    # -----------------------------------------------------

    st.subheader("📊 Equipment Summary")

    total_equipment = len(df)

    available_equipment = len(
        df[df["Maintenance Status"] != "Under Maintenance"]
    )

    equipment_alerts = len(
        df[df["Condition"].isin(["Warning", "Critical"])]
    )

    average_availability = df["Availability"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Equipment",
        total_equipment
    )

    col2.metric(
        "Available Equipment",
        available_equipment
    )

    col3.metric(
        "Equipment Alerts",
        equipment_alerts
    )

    col4.metric(
        "Average Availability",
        f"{average_availability:.1f}%"
    )

    st.divider()

    # -----------------------------------------------------
    # EQUIPMENT TABLE
    # -----------------------------------------------------

    st.subheader("📋 Equipment Records")

    st.dataframe(
        df,
        use_container_width=True
    )

    # -----------------------------------------------------
    # FILTER
    # -----------------------------------------------------

    st.subheader("🔎 Filter Equipment")

    selected_types = st.multiselect(
        "Equipment Type",
        options=df["Equipment Type"].unique(),
        default=df["Equipment Type"].unique()
    )

    filtered_df = df[
        df["Equipment Type"].isin(selected_types)
    ]

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    # -----------------------------------------------------
    # EQUIPMENT ALERTS
    # -----------------------------------------------------

    alert_df = filtered_df[
        (filtered_df["Condition"].isin(["Warning", "Critical"]))
        |
        (filtered_df["Maintenance Status"].isin(
            ["Due", "Overdue", "Under Maintenance"]
        ))
        |
        (filtered_df["Availability"] < 80)
    ]

    if not alert_df.empty:

        st.subheader("🚨 Equipment Alerts")

        for _, row in alert_df.iterrows():

            st.warning(
                f"Equipment **{row['Equipment ID']}** | "
                f"Type: {row['Equipment Type']} | "
                f"Condition: **{row['Condition']}** | "
                f"Temperature: {row['Temperature']} °C | "
                f"Vibration: {row['Vibration']} | "
                f"Maintenance: {row['Maintenance Status']} | "
                f"Availability: {row['Availability']:.1f}%"
            )

    # -----------------------------------------------------
    # CONDITION ANALYSIS
    # -----------------------------------------------------

    st.subheader("📈 Equipment Condition Analysis")

    condition_counts = (
        filtered_df["Condition"]
        .value_counts()
        .rename_axis("Condition")
        .reset_index(name="Number of Equipment")
    )

    st.bar_chart(
        condition_counts.set_index("Condition")
    )

    # -----------------------------------------------------
    # AVAILABILITY ANALYSIS
    # -----------------------------------------------------

    st.subheader("📊 Equipment Availability")

    availability_df = filtered_df[
        ["Equipment ID", "Availability"]
    ].set_index("Equipment ID")

    st.bar_chart(
        availability_df
    )
