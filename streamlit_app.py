import streamlit as st

from usajobs_api import fetch_usajobs
from orchestrator import run_pipeline
from utils.tracking import log_application


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="AI Job Hunt Assistant",
    page_icon="💼",
    layout="wide"
)


# --------------------------------
# TITLE
# --------------------------------

st.title("💼 AI Job Hunt Assistant")

st.write("""
Search USAJobs, select a job, and let AI agents help you:

- Analyze the job description
- Tailor your resume
- Generate a cover letter
- Create a professional outreach message
- Track your applications
""")


# --------------------------------
# JOB SEARCH INPUTS
# --------------------------------

st.subheader("🔍 Search for Jobs")

col1, col2 = st.columns(2)

with col1:
    keyword = st.text_input(
        "Job Keyword",
        value="Business Analyst"
    )

with col2:
    location = st.text_input(
        "Location",
        value="New York"
    )


# --------------------------------
# SEARCH JOBS
# --------------------------------

if st.button("Search Jobs", type="primary"):

    if not keyword.strip():
        st.warning("Please enter a job keyword.")

    else:
        with st.spinner("Searching USAJobs..."):

            jobs = fetch_usajobs(
                keyword=keyword,
                location=location,
                results_per_page=10
            )

        # Store jobs in session state
        st.session_state["jobs"] = jobs

        # Clear old analysis when searching again
        st.session_state.pop("result", None)
        st.session_state.pop("selected_job", None)


# --------------------------------
# DISPLAY JOB RESULTS
# --------------------------------

if "jobs" in st.session_state:

    jobs = st.session_state["jobs"]

    if not jobs:

        st.warning("No jobs found. Try another keyword or location.")

    else:

        st.subheader("📋 Available Jobs")

        job_options = {}

        for index, job in enumerate(jobs):

            job_data = job.get("MatchedObjectDescriptor", {})

            title = job_data.get(
                "PositionTitle",
                "Unknown Position"
            )

            agency = job_data.get(
                "OrganizationName",
                "Unknown Agency"
            )

            # Unique label for each job
            label = f"{index + 1}. {title} — {agency}"

            job_options[label] = index


        # --------------------------------
        # JOB SELECTION
        # --------------------------------

        selected_label = st.selectbox(
            "Select a Job to Analyze",
            list(job_options.keys())
        )

        selected_index = job_options[selected_label]

        selected_job = jobs[selected_index]

        selected_job_data = selected_job.get(
            "MatchedObjectDescriptor",
            {}
        )


        # --------------------------------
        # SHOW SELECTED JOB DETAILS
        # --------------------------------

        st.subheader("💼 Selected Job")

        st.write(
            f"**Position:** "
            f"{selected_job_data.get('PositionTitle', 'Unknown')}"
        )

        st.write(
            f"**Agency:** "
            f"{selected_job_data.get('OrganizationName', 'Unknown')}"
        )

        st.write(
            f"**Department:** "
            f"{selected_job_data.get('DepartmentName', 'Not available')}"
        )


        # --------------------------------
        # RUN AI WORKFLOW
        # --------------------------------

        if st.button("🤖 Analyze Selected Job"):

            with st.spinner(
                "AI agents are analyzing the job and creating application materials..."
            ):

                result = run_pipeline(selected_job)

            # Store data so it remains available
            # when Streamlit reruns the application
            st.session_state["result"] = result
            st.session_state["selected_job"] = selected_job

            st.success("Analysis completed successfully!")


# --------------------------------
# DISPLAY AI RESULT
# --------------------------------

if "result" in st.session_state:

    st.subheader("✨ AI Generated Application Materials")

    result = st.session_state["result"]

    st.markdown(str(result))


# --------------------------------
# APPLICATION TRACKING
# --------------------------------

if (
    "result" in st.session_state
    and "selected_job" in st.session_state
):

    st.divider()

    st.subheader("📌 Application Tracking")

    st.write(
        "Once you have applied for this job, click the button below "
        "to save the application details."
    )

    if st.button("✅ Mark as Applied"):

        job_data = (
            st.session_state["selected_job"]
            .get("MatchedObjectDescriptor", {})
        )

        job_title = job_data.get(
            "PositionTitle",
            "Unknown Position"
        )

        agency = job_data.get(
            "OrganizationName",
            "Unknown Agency"
        )

        # Save application details in CSV
        log_application(
            job_title=job_title,
            agency=agency,
            resume_summary=str(
                st.session_state["result"]
            )
        )

        st.success(
            f"Application for '{job_title}' has been logged successfully!"
        )

        st.info(
            "You can find the saved details in: "
            "data/applications_log.csv"
        )