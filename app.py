#Login portal
import streamlit as st
users = { "admin": {"password": "admin123", "role": "Administrator"},
         "safety": {"password": "safety123", "role": "Safety Officer"},
         "mining": {"password": "mining123", "role": "Mining Engineer"},
         "maintenance": {"password": "maintanace123", "role": "Maintenance Engineer"},
         "manager": {"password": "manager123", "role": "Manager" }}

permissions = {"Administrator": ["View dashboard", "Worker safety data", "Safety incidents", "Equipment data", "Maintenance data", "Risk assessment","Generate reports","Manage users"],
               "Safety Officer": ["View dashboard", "Worker safety data","Safety incidents", "Risk assessment", "Generate reports"],
               "Mining Engineer": ["View dashboard", "Worker safety data", "Safety incidents", "Equipment data", "Maintenance data", "Risk assessment", "Generate reports"],
               "Maintenance Engineer": ["View dashboard", "Equipment data", "Maintenance data", "Generate reports"],
               "Manager": ["View dashboard", "Worker safety data", "Safety incidents", "Equipment data", "Maintenance data", "Risk assessment", "Generate reports"]}

st.title("Mining Health, Safety and Equipment Monitoring Application")

st.subheader("Login")

username = st.text_input("Enter your username:")
password = st.text_input("Enter your password:", type="password")

if st.button("Login"):
    if username in users:
        if password == users[username]["password"]:
            role = users[username]["role"]
            st.success("Login Successful")
            st.write("Role:", role)
            # Show only functions allowed for the user's role
            st.subheader("Available Functions")

            if "View dashboard" in permissions[role]:
                st.write("✓ View dashboard")

            if "Worker safety data" in permissions[role]:
                st.write("✓ Worker safety data")

            if "Safety incidents" in permissions[role]:
                st.write("✓ Safety incidents")

            if "Equipment data" in permissions[role]:
                st.write("✓ Equipment data")

            if "Maintenance data" in permissions[role]:
                st.write("✓ Maintenance data")

            if "Risk assessment" in permissions[role]:
                st.write("✓ Risk assessment")

            if "Generate reports" in permissions[role]:
                st.write("✓ Generate reports")

            if "Manage users" in permissions[role]:
                st.write("✓ Manage users")
        else:
            st.error("Incorrect Password")
    else:
        st.error("Username not found")
