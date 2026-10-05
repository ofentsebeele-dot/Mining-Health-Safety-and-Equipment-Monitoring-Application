import streamlit as st
import pandas as pd

def calculate_risk(likelihood, consequence):
    score = likelihood * consequence
    if score >= 15:
        return score, "Critical", "🔴 Red", "Immediate shutdown or high-level executive intervention required. Implement mandatory controls before work continues."
    elif score >= 10:
        return score, "High", "🟠 Orange", "High priority. Detailed risk control plan required. Senior supervisor oversight mandatory."
    elif score >= 5:
        return score, "Medium", "🟡 Yellow", "Medium priority. Apply standard operating procedures and personal protective equipment (PPE)."
    else:
        return score, "Low", "🟢 Green", "Low priority. Acceptable risk level. Continue monitoring under routine safety controls."

def render_risk_assessment_page():
    st.title("⚠️ Mining Risk Assessment Matrix")
    st.markdown("Evaluate task and operational hazards using the standard 5x5 Risk Assessment Matrix ($Likelihood \\times Consequence$).")

    if "risk_assessments" not in st.session_state:
        st.session_state.risk_assessments = pd.DataFrame([
            {
                "Hazard ID": "HAZ-001",
                "Hazard Description": "Methane gas buildup in Underground Shaft 2",
                "Likelihood": 4,
                "Consequence": 5,
                "Risk Score": 20,
                "Risk Level": "Critical",
                "Mitigation Strategy": "Install continuous automated gas monitors and forced ventilation fans."
            },
            {
                "Hazard ID": "HAZ-002",
                "Hazard Description": "Conveyor belt roller overheating in Processing Plant",
                "Likelihood": 3,
                "Consequence": 3,
                "Risk Score": 9,
                "Risk Level": "Medium",
                "Mitigation Strategy": "Schedule bi-weekly thermal imaging inspections and lubrication."
            }
        ])

    df = st.session_state.risk_assessments

    # KPI Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Evaluated Hazards", len(df))
    col2.metric("Critical Hazards", len(df[df["Risk Level"] == "Critical"]))
    col3.metric("High Risks", len(df[df["Risk Level"] == "High"]))
    col4.metric("Medium / Low Risks", len(df[df["Risk Level"].isin(["Medium", "Low"])]))

    st.divider()

    # Hazard Risk Calculator Form
    with st.expander("➕ Perform New Hazard Risk Assessment", expanded=True):
        with st.form("risk_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)

            with col_a:
                hazard_id = f"HAZ-{len(df) + 1:03d}"
                st.text_input("Hazard ID", value=hazard_id, disabled=True)
                hazard_desc = st.text_area("Hazard Description", placeholder="Describe the potential hazard, equipment, or working environment...")
                
            with col_b:
                likelihood = st.slider("Likelihood Rating (1 = Rare, 5 = Almost Certain)", min_value=1, max_value=5, value=3)
                consequence = st.slider("Consequence Rating (1 = Insignificant, 5 = Catastrophic)", min_value=1, max_value=5, value=3)
                mitigation = st.text_area("Proposed Mitigation / Control Action", placeholder="Detail the controls required to mitigate this hazard...")

            submit_btn = st.form_submit_button("Calculate & Log Risk")

            if submit_btn:
                if not hazard_desc.strip():
                    st.error("Please enter a hazard description before submitting.")
                else:
                    score, level, badge, action = calculate_risk(likelihood, consequence)
                    
                    new_hazard = {
                        "Hazard ID": hazard_id,
                        "Hazard Description": hazard_desc,
                        "Likelihood": likelihood,
                        "Consequence": consequence,
                        "Risk Score": score,
                        "Risk Level": level,
                        "Mitigation Strategy": mitigation
                    }

                    st.session_state.risk_assessments = pd.concat([
                        st.session_state.risk_assessments,
                        pd.DataFrame([new_hazard])
                    ], ignore_index=True)

                    st.success(f"Hazard {hazard_id} evaluated with a Risk Score of **{score}** ({level} Risk).")
                    
                    if level in ["Critical", "High"]:
                        st.error(f"🚨 **HIGH RISK WARNING**: {action}")
                    else:
                        st.info(f"ℹ️ **Action Plan**: {action}")

    st.subheader("📋 Hazard Evaluation Registry")
    st.dataframe(df, use_container_width=True)