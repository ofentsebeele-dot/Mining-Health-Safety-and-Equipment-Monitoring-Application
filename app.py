#Login portal
import streamlit as st
users = { "admin": {"password": "admin123", "role": "Administrator"},
         "safety": {"password": "safety123", "role": "Safety Officer"},
         "mining": {"password": "mining123", "role": "Mining Engineer"},
         "maintenance": {"password": "maintanace123", "role": "Maintenance Engineer"},
         "manager": {"password": "manager123", "role": "Manager" }}
username = input("enter your username:")
password = input("enter your password:")
if username in users:
    if password == users[username]["password"]:
        role = users[username]["role"]
        print("Login Successful")
        print("Role",role)
    else:
        print("Incorrect Password")
else:
    print("Username not found")
