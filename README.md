# ATS System

## Project Description
The ATS System is a web-based Applicant Tracking System built with the Django framework. It helps manage the entire recruitment process, from creating job postings to tracking candidates and scheduling interviews.

## Features
- **Job Management**: Recruiters can create, view, edit, and publish job postings. Each job post can be assigned to a department and includes details like title, location, description, requirements, responsibilities, and salary range.
- **Candidate Management**:
  - Add and track candidates manually or by parsing a resume.
  - View a detailed profile for each candidate, including personal information, resume, and cover letter.
  - Manage a candidate's skills, education, and work experience.
  - Progress candidates through different recruitment stages, such as `new`, `screening`, `interview`, `technical`, `final`, `offer`, `hired`, and `rejected`.
- **Recruiter Tools**:
  - **Notes**: Recruiters can add private notes to a candidate's profile.
  - **Interviews**: The system allows for scheduling interviews with candidates, specifying the date, time, duration, and interviewers.
  - **Email Templates**: Recruiters can create and use email templates for common communication with candidates, such as interview invitations or rejections.

## Technical Stack
- **Backend**: Django
- **Database**: SQLite3
- **Frontend**: HTML with Bootstrap 5

## Installation and Setup

### Prerequisites
- Python (3.x recommended)
- Django (5.1.7)

### Steps
1.  **Clone the repository**: (Assuming the user knows how to clone a repository from their system)
2.  **Install dependencies**: `pip install Django`
3.  **Database Setup**: The project uses an SQLite database. The database schema is already defined in the migration files for the `jobs`, `candidates`, and `recruiters` apps. Run the migrations to set up the database tables:
    `python manage.py migrate`
4.  **Create a superuser**: To access the admin interface, create a superuser:
    `python manage.py createsuperuser`
5.  **Run the development server**:
    `python manage.py runserver`

The application will now be running at `http://127.0.0.1:8000/`.

## Application Structure
The project is composed of three main apps:
- `jobs`: Manages job postings and departments.
- `candidates`: Manages candidate profiles, including their skills, education, and work experience.
- `recruiters`: Provides tools for recruiters, such as adding notes, scheduling interviews, and sending emails.

## Database Schema
The database contains the following key tables (models):
- `JobPost`: Stores information about job openings.
- `Department`: Categorizes job posts.
- `Candidate`: Stores a candidate's personal and application details, with a foreign key to `JobPost`.
- `CandidateSkill`, `CandidateEducation`, `CandidateWorkExperience`: Related to `Candidate`, these tables store detailed information about a candidate's background.
- `Note`: Allows recruiters to add notes to a `Candidate`'s profile.
- `Interview`: Schedules interviews for a `Candidate` with a `JobPost` and multiple `interviewers` (users).
- `EmailTemplate`: Stores reusable templates for sending emails to candidates.
