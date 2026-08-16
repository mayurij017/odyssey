from crewai import Agent, Task, LLM
from utils.config import GEMINI_API_KEY


llm = LLM(
    model="gemini/gemini-flash-latest",
    temperature=0.3,
    api_key=GEMINI_API_KEY
)


def get_resume_cl_agent():
    return Agent(
        role="Resume & Cover Letter Writer",
        goal="Customize application materials to match job descriptions",
        backstory="""
        You're an expert in professional writing and tailoring
        resumes for job applications, especially in government
        and technology roles.
        """,
        llm=llm,
        verbose=True
    )


def create_resume_cl_task(agent, resume_text, context):
    return Task(
        description=f"""
        Using the previous JD analysis, tailor the candidate's
        application materials.

        Candidate Resume:
        {resume_text}

        Generate:

        1. Updated Professional Summary
        2. Key Skills to Highlight
        3. Personalized Cover Letter

        Make everything specifically relevant to the analyzed position.
        """,
        expected_output="""
        ## RESUME SUMMARY
        A tailored professional summary.

        ## KEY SKILLS
        Relevant skills to highlight.

        ## COVER LETTER
        A personalized cover letter.
        """,
        agent=agent,
        context=context,
        output_file="data/resume_agent_output.txt"
    )