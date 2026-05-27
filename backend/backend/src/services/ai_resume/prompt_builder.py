def build_ats_analysis_prompt(
    resume_text: str,
    target_role: str,
    experience_level: str,
    job_description: str,
) -> str:
    """
    Builds structured ATS analysis prompt for OpenAI.
    """

    return f"""
You are an expert ATS (Applicant Tracking System) analyzer,
technical recruiter, and resume reviewer.

Analyze the candidate's resume against the provided job description.

Your task:
1. Evaluate ATS compatibility
2. Analyze skills match
3. Identify missing keywords
4. Review projects
5. Check resume hygiene
6. Give actionable recommendations

IMPORTANT RULES:
- Return ONLY valid JSON
- No markdown
- No explanations outside JSON
- atsScore must be between 0-100
- All scores must be between 0-100
- Keep feedback concise and professional

Return response in EXACT schema below:

{{
  "atsScore": 72,
  "summary": "Strong backend-focused resume with relevant technical skills but lacks keyword optimization for ATS systems.",
  "scoreBreakdown": {{
    "skillsMatch": 80,
    "experienceMatch": 68,
    "formattingScore": 75,
    "keywordDensity": 70
  }},
  "skillsAnalysis": {{
    "strongSkills": [
      "Python",
      "FastAPI",
      "PostgreSQL"
    ],
    "missingSkills": [
      "Docker",
      "AWS"
    ],
    "deprioritizedSkills": [
      "jQuery"
    ]
  }},
  "projectFeedback": [
    {{
      "projectName": "AI Interview Platform",
      "rating": "Excellent",
      "feedback": "Strong real-world backend architecture and AI integration."
    }}
  ],
  "projectRecommendations": [
    "Add measurable impact to projects",
    "Include deployment links"
  ],
  "hygieneCheck": {{
    "grammarIssues": [],
    "hasLinkedIn": true,
    "hasGithub": true,
    "hasPortfolio": false
  }}
}}

CANDIDATE TARGET ROLE:
{target_role}

CANDIDATE EXPERIENCE LEVEL:
{experience_level}

JOB DESCRIPTION:
{job_description}

RESUME CONTENT:
{resume_text}
"""