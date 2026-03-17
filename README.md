# P2P Modernization Dashboard

A Flask-based web dashboard for displaying and editing portfolio, projects, and sub-projects information.

## Features

- **View Dashboard**: Displays portfolio name and description, projects, and sub-projects
- **Status & Health Overview**: Dedicated section showing project status counts and health indicators
- **Project Summary Table**: Quick overview of all projects with key details
- **Edit Projects**: Click "Edit Project" to modify project details including descriptions, dates, status, and health
- **Edit Sub-Projects**: Click "Edit" on sub-projects to modify their details
- **Real-time Updates**: Changes are saved directly to data.json and reflected immediately
- **Responsive Design**: Clean, mobile-friendly interface using Bootstrap

## Data Fields

Each project and sub-project includes:
- Name and description
- Start and end dates
- Requested deployment dates
- Status (Active, On Hold, Completed, Cancelled)
- Health (Green - On Track, Yellow - At Risk, Red - Critical Issues)

## Installation

1. Install Python 3.7+ if not already installed
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

Run the Flask app:
```
python app.py
```

The dashboard will be available at http://localhost:5000

## Usage

1. **View Projects**: The main dashboard shows all projects and their sub-projects
2. **Edit a Project**: Click the "Edit Project" button on any project card
3. **Edit a Sub-Project**: Click the "Edit" button on any sub-project
4. **Save Changes**: Fill out the form and click "Save Changes" to update the data
5. **Cancel**: Click "Cancel" to return to the dashboard without saving

## Data Structure

The application reads and writes data to `data.json` which contains:
- projects: array of project objects
- Each project has: id, name, status, health, start_date, end_date, deployment_date, description, sub_projects

## API Endpoints

- `/`: Main dashboard view
- `/edit/<project_id>`: Edit a specific project
- `/edit/<project_id>/sub/<sub_id>`: Edit a specific sub-project
- `/api/projects`: JSON API for project dataecho "# P2P-modernization-Portfolio-Status-dashboard" >> README.md
git remote add origin https://github.com/JenniferDavis18/p2p-dashboard.git


