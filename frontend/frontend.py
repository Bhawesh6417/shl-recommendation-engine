import streamlit as st
import requests

# URL to your FastAPI backend
API_URL = "http://localhost:8000/search"

# Streamlit UI
st.set_page_config(page_title="SHL Recommendation Engine", layout="wide")
st.title(" SHL Recommendation Engine")

job_description = st.text_area("Enter Job Description:", height=200)

if st.button("Get Recommendations"):
    if not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        try:
            response = requests.get(API_URL, params={"query": job_description})
            response.raise_for_status()  # Raise error if not 2xx

            data = response.json()
            recommendations = data.get("recommendations", [])

            if recommendations:
                st.subheader("✅ Recommended Assessments/Skills:")
                for idx, rec in enumerate(recommendations, 1):
                    st.markdown(f"{idx}. {rec}")
            else:
                st.info("No recommendations found.")
        except requests.exceptions.RequestException as e:
            st.error(f" API request failed: {e}")
        except Exception as e:
            st.error(f" Something went wrong: {e}")
