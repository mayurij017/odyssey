from crewai import Crew, Process

from agents.jd_analyst import (
    get_jd_analyst_agent,
    create_jd_analysis_task
)

from agents.resume_cl_agent import (
    get_resume_cl_agent,
    create_resume_cl_task
)

from agents.messaging_agent import (
    get_messaging_agent,
    create_messaging_task
)


def run_pipeline(selected_job):

    # --------------------------------
    # Extract selected job information
    # --------------------------------

    job_data = selected_job["MatchedObjectDescriptor"]

    job_title = job_data.get(
        "PositionTitle",
        "Unknown Position"
    )

    agency = job_data.get(
        "OrganizationName",
        "Unknown Agency"
    )

    job_summary = (
        job_data
        .get("UserArea", {})
        .get("Details", {})
        .get("JobSummary", "")
    )

    # --------------------------------
    # Read resume
    # --------------------------------

    with open(
        "data/sample_resume.txt",
        "r",
        encoding="utf-8"
    ) as file:

        resume_text = file.read()

    # --------------------------------
    # JD Agent
    # --------------------------------

    jd_agent = get_jd_analyst_agent()

    jd_task = create_jd_analysis_task(
        jd_agent,
        job_summary
    )

    # --------------------------------
    # Resume Agent
    # --------------------------------

    resume_agent = get_resume_cl_agent()

    resume_task = create_resume_cl_task(
        resume_agent,
        resume_text,
        context=[jd_task]
    )

    # --------------------------------
    # Messaging Agent
    # --------------------------------

    messaging_agent = get_messaging_agent()

    messaging_task = create_messaging_task(
        messaging_agent,
        job_title,
        agency,
        context=[jd_task, resume_task]
    )

    # --------------------------------
    # Crew
    # --------------------------------

    crew = Crew(
        agents=[
            jd_agent,
            resume_agent,
            messaging_agent
        ],

        tasks=[
            jd_task,
            resume_task,
            messaging_task
        ],

        process=Process.sequential,

        verbose=True
    )

    result = crew.kickoff()

    return result