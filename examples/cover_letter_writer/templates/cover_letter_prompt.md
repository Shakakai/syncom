# Instructions
You must write the highest-quality cover letter possible for the user.
Make sure to highlight the relevant skills listed below that match the job description.
Be sure to use the applicant info, skills, job description, and resume included to write the most compelling cover letter possible.

# Applicant
- Name: {{ applicant.name }}
- Email: {{ applicant.email }}
- Phone: {{ applicant.phone }}
- Address: {{ applicant.address }}

# Skills
{% for skill in skills %}
- {{ skill.name }}: {{ skill.description }} ({{ skill.job }}){% endfor %}

# Job Description
{{ job_description }}

# Resume
{{ resume }}