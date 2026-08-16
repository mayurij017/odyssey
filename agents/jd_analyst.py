from crewai import Agent, Task, LLM
from utils.config import GEMINI_API_KEY


llm = LLM(
    model="gemini/gemini-flash-latest",
    temperature=0.2,
    api_key=GEMINI_API_KEY
)


def get_jd_analyst_agent():
    return Agent(
        role="JD Analyst",
        goal="Understand and summarize government job postings",
        backstory="""
        You're an expert in job market analysis with a focus
        on US federal job listings.
        """,
        llm=llm,
        verbose=True
    )


def create_jd_analysis_task(agent, job_description):
    return Task(
        description=f"""
        Analyze the following USAJobs job posting and extract:

        - A summary of the role
        - Key skills required
        - Specific qualifications or eligibility
        - Main responsibilities

        Job Description:
        {job_description}
        """,
        expected_output="""
        A structured markdown analysis with these sections:

        ## Role Summary
        ## Qualifications
        ## Required Skills
        ## Responsibilities
        """,
        agent=agent,
        output_file="data/report.md"
    )