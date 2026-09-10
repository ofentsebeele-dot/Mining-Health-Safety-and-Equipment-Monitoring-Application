import streamlit as st
users = { "admin": {"password": "admin123", "role": "Administrator"},
         "safety": {"password": "safety123", "role": "Safety Officer"},
         "mining": {"password": "mining123", "role": "Mining Engineer"},
         "maintenance": {"password": "maintanace123", "role": "Maintenance Engineer"},
         "manager": {"password": "manager123", "role": "Manager" }}
st.title("Mining Health, Safety and Equipment Monitoring Application")
st.subheader("Login")
username = st.text_input("enter your username:")
password = st.text_input("enter your password:")
if st.username in users:
    if password == users[username]["password"]:
        role = users[username]["role"]
        print("Login Successful")
        print("Role",role)
    else:
        st.error("Incorrect Password")
else:
    st.error("Username not found")
