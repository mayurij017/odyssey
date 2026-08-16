from crewai import Agent, Task, LLM
from utils.config import GEMINI_API_KEY


llm = LLM(
    model="gemini/gemini-flash-latest",
    temperature=0.4,
    api_key=GEMINI_API_KEY
)


def get_messaging_agent():
    return Agent(
        role="Professional Messaging Specialist",
        goal="""
        Create concise and professional job application
        messages based on job and candidate information.
        """,
        backstory="""
        You are an expert career communication specialist who
        writes professional outreach and follow-up messages.
        """,
        llm=llm,
        verbose=True
    )


def create_messaging_task(agent, job_title, agency, context):
    return Task(
        description=f"""
        Based on the previous job analysis and tailored application
        materials, write a concise professional outreach message.

        Job Title: {job_title}
        Agency: {agency}

        The message should:

        - Express interest in the position
        - Briefly mention relevant qualifications
        - Be professional and concise
        - Express interest in contributing to the organization

        Keep it under 200 words.
        """,
        expected_output="""
        ## SUBJECT
        A concise email subject.

        ## MESSAGE
        A polished professional outreach message.
        """,
        agent=agent,
        context=context,
        output_file="data/message_output.txt"
    )