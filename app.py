# Login portal
import streamlit as st
from worker_health import render_worker_health_page

# Preserve group members' exact user and permission dictionaries
users = {
    "admin": {"password": "admin123", "role": "Administrator"},
    "safety": {"password": "safety123", "role": "Safety Officer"},
    "mining": {"password": "mining123", "role": "Mining Engineer"},
    "maintenance": {"password": "maintenance123", "role": "Maintenance Engineer"},
    "manager": {"password": "manager123", "role": "Manager"},
}

permissions = {
    "Administrator": [
        "View dashboard",
        "Worker safety data",
        "Safety incidents",
        "Equipment data",
        "Maintenance data",
        "Risk assessment",
        "Generate reports",
        "Manage users",
    ],
    "Safety Officer": [
        "View dashboard",
        "Worker safety data",
        "Safety incidents",
        "Risk assessment",
        "Generate reports",
    ],
    "Mining Engineer": [
        "View dashboard",
        "Worker safety data",
        "Safety incidents",
        "Equipment data",
        "Maintenance data",
        "Risk assessment",
        "Generate reports",
    ],
    "Maintenance Engineer": [
        "View dashboard",
        "Equipment data",
        "Maintenance data",
        "Generate reports",
    ],
    "Manager": [
        "View dashboard",
        "Worker safety data",
        "Safety incidents",
        "Equipment data",
        "Maintenance data",
        "Risk assessment",
        "Generate reports",
    ],
}

# Session state management for login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None


def login_screen():
    st.title("Mining Health, Safety and Equipment Monitoring Application")
    st.subheader("Login")

    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")

    if st.button("Login"):
        if username in users:
            if password == users[username]["password"]:
                st.session_state.logged_in = True
                st.session_state.role = users[username]["role"]
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Incorrect Password")
        else:
            st.error("Username not found")


def main_dashboard():
    role = st.session_state.role

    # Sidebar containing your team's exact permission features as dynamic choices
    st.sidebar.title("📌 Main Menu")
    st.sidebar.write(f"**Logged in as:** {role}")

    allowed_functions = permissions.get(role, [])
    selected_page = st.sidebar.radio("Available Functions:", allowed_functions)

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()

    # Route selected page based on your team's permission list
    if selected_page == "View dashboard":
        st.title("📊 Central Dashboard")
        st.write("Welcome to the Mining Health, Safety, and Equipment System.")

    elif selected_page == "Worker safety data":
        # Calls your worker_health.py page function
        render_worker_health_page()

    elif selected_page == "Safety incidents":
        st.title("🚨 Safety Incidents")
        st.info("Safety incident tracking module.")

    elif selected_page == "Equipment data":
        st.title("⚙️ Equipment Data")
        st.info("Equipment condition monitoring module.")

    elif selected_page == "Maintenance data":
        st.title("🛠️ Maintenance Data")
        st.info("Maintenance scheduling and logs.")

    elif selected_page == "Risk assessment":
        st.title("⚠️ Risk Assessment")
        st.info("Risk matrix and evaluation tool.")

    elif selected_page == "Generate reports":
        st.title("📄 Generate Reports")
        st.info("System reporting tools.")

    elif selected_page == "Manage users":
        st.title("👤 Manage Users")
        st.info("User administration panel.")


# Application Flow
if not st.session_state.logged_in:
    login_screen()
else:
    main_dashboard()