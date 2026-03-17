from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import os

app = Flask(__name__)

def load_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    # Ensure every project has a resources list
    for project in data.get('projects', []):
        if 'resources' not in project:
            project['resources'] = []
    return data

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def dashboard():
    # Load data from data.json
    data = load_data()

    # For now, assume the entire data is one portfolio
    portfolio = {
        "name": "P2P Modernization Portfolio",
        "description": "The P2P Modernization Program is a multi‑year initiative to transition Seaboard Foods from legacy IBMi‑based Procure‑to‑Pay applications to a modern, scalable P2P platform. The program is being delivered through a wave‑based model, beginning with a pilot module (Wave 0) to validate delivery approach, requirements quality, design standards, testing processes, and stakeholder engagement before scaling across additional modules.",
        "projects": data.get('projects', [])
    }

    return render_template('dashboard.html', portfolio=portfolio)

@app.route('/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    data = load_data()
    projects = data.get('projects', [])

    # Find the project
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        return "Project not found", 404

    if request.method == 'POST':
        # Update project data
        project['name'] = request.form.get('name', project['name'])
        project['description'] = request.form.get('description', project['description'])
        project['start_date'] = request.form.get('start_date', project['start_date'])
        project['end_date'] = request.form.get('end_date', project['end_date'])
        project['deployment_date'] = request.form.get('deployment_date', project['deployment_date'])
        project['status'] = request.form.get('status', project['status'])
        project['health'] = request.form.get('health', project['health'])

        # Save changes
        save_data(data)
        return redirect(url_for('dashboard'))

    return render_template('edit_project.html', project=project)

@app.route('/edit/<int:project_id>/sub/<int:sub_id>', methods=['GET', 'POST'])
def edit_subproject(project_id, sub_id):
    data = load_data()
    projects = data.get('projects', [])

    # Find the project
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        return "Project not found", 404

    # Find the sub-project
    sub_project = next((sp for sp in project.get('sub_projects', []) if sp['id'] == sub_id), None)
    if not sub_project:
        return "Sub-project not found", 404

    if request.method == 'POST':
        # Update sub-project data
        sub_project['name'] = request.form.get('name', sub_project['name'])
        sub_project['description'] = request.form.get('description', sub_project['description'])
        sub_project['start_date'] = request.form.get('start_date', sub_project['start_date'])
        sub_project['end_date'] = request.form.get('end_date', sub_project['end_date'])
        sub_project['deployment_date'] = request.form.get('deployment_date', sub_project['deployment_date'])
        sub_project['status'] = request.form.get('status', sub_project['status'])
        sub_project['health'] = request.form.get('health', sub_project['health'])

        # Save changes
        save_data(data)
        return redirect(url_for('dashboard'))

    return render_template('edit_subproject.html', project=project, sub_project=sub_project)

@app.route('/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    data = load_data()
    projects = data.get('projects', [])

    # Remove the project
    data['projects'] = [p for p in projects if p['id'] != project_id]

    # Save changes
    save_data(data)
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:project_id>/sub/<int:sub_id>', methods=['POST'])
def delete_subproject(project_id, sub_id):
    data = load_data()
    projects = data.get('projects', [])

    # Find the project
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        return "Project not found", 404

    # Find and remove the sub-project
    project['sub_projects'] = [sp for sp in project.get('sub_projects', []) if sp['id'] != sub_id]

    # Save changes
    save_data(data)
    return redirect(url_for('dashboard'))

@app.route('/api/projects')
def get_projects():
    data = load_data()
    return jsonify(data.get('projects', []))

# ── Resource Allocation Routes ──────────────────────────────────────────────

@app.route('/project/<int:project_id>/resources/create', methods=['GET', 'POST'])
def create_resource(project_id):
    data = load_data()
    project = next((p for p in data.get('projects', []) if p['id'] == project_id), None)
    if not project:
        return "Project not found", 404

    if request.method == 'POST':
        resources = project.get('resources', [])
        existing_ids = [r['id'] for r in resources] if resources else []
        new_id = max(existing_ids) + 1 if existing_ids else 1
        new_resource = {
            'id': new_id,
            'name': request.form.get('name', ''),
            'role': request.form.get('role', ''),
            'allocation': request.form.get('allocation', ''),
            'start_date': request.form.get('start_date', ''),
            'end_date': request.form.get('end_date', '')
        }
        project['resources'] = resources + [new_resource]
        save_data(data)
        return redirect(url_for('dashboard'))

    return render_template('create_resource.html', project=project)

@app.route('/project/<int:project_id>/resources/<int:resource_id>/edit', methods=['GET', 'POST'])
def edit_resource(project_id, resource_id):
    data = load_data()
    project = next((p for p in data.get('projects', []) if p['id'] == project_id), None)
    if not project:
        return "Project not found", 404

    resource = next((r for r in project.get('resources', []) if r['id'] == resource_id), None)
    if not resource:
        return "Resource not found", 404

    if request.method == 'POST':
        resource['name'] = request.form.get('name', resource['name'])
        resource['role'] = request.form.get('role', resource['role'])
        resource['allocation'] = request.form.get('allocation', resource['allocation'])
        resource['start_date'] = request.form.get('start_date', resource['start_date'])
        resource['end_date'] = request.form.get('end_date', resource['end_date'])
        save_data(data)
        return redirect(url_for('dashboard'))

    return render_template('edit_resource.html', project=project, resource=resource)

@app.route('/project/<int:project_id>/resources/<int:resource_id>/delete', methods=['POST'])
def delete_resource(project_id, resource_id):
    data = load_data()
    project = next((p for p in data.get('projects', []) if p['id'] == project_id), None)
    if not project:
        return "Project not found", 404

    project['resources'] = [r for r in project.get('resources', []) if r['id'] != resource_id]
    save_data(data)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
