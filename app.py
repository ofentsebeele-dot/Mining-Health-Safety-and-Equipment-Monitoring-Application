import streamlit as st
st.title("Mining Health, Safety and Equipment Monitoring Application")
st.write("Welcome to the Application")
st.success("Streamlit is working")
#Login portal
users = { "admin": {"password": "admin123", "role": "Administrator"},
         "safety": {"password": "safety123", "role": "Safety Officer"},
         "mining": {"password": "mining123", "role": "Mining Engineer"},
         "maintenance": {"password": "maintanace123", "role": "Maintenance Engineer"},
         "manager": {"password": "manager123", "role": "Manager" }}
