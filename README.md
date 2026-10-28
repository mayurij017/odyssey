# ODYSSEY: AI-Powered Job Application Assistant

A multi-agent system that finds jobs, analyzes them against your profile, tailors your resume and cover letter, and helps automate LinkedIn outreach, all from a Streamlit dashboard.

## Features
- **Job discovery** through the USAJobs API
- **Job analysis:** an agent breaks down each posting's requirements
- **Tailored applications:** resume and cover letter customized per job
- **LinkedIn outreach:** drafts and automates networking messages
- **Application tracking** in one UI

## Tech Stack
Python · CrewAI · Google Gemini · Streamlit · REST APIs (USAJobs)

## Architecture
```
Streamlit UI
     │
     ▼
CrewAI Crew ──► Job Description Analyst agent       (parses the job description)
            ├─► Resume and Cover letter generator   (matches resume to the role)
            └─► Outreach agent                      (LinkedIn messages)
     │
     ▼
USAJobs API + Gemini
```


## Usage
1. Upload or paste your resume
2. Search for jobs by keyword and location
3. Select a job and let the agents analyze it
4. Review the tailored resume, cover letter, and outreach message
5. Track the application status


## Limitations
- Always review generated content before sending
- LinkedIn automation should follow LinkedIn's terms of service
- Job data currently comes from USAJobs only

## Future Improvements
- Add more job sources
- Resume-to-job match scoring
- Email and calendar integration for follow-ups

## Author
Mayuri Joshi 
