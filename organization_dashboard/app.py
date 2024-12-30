from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Create a folder for storing uploaded profile pictures
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Data storage (for demonstration purposes)
organizations = []

# Route for the registration page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get form data
        org_name = request.form.get('org_name')
        org_location = request.form.get('org_location')
        team_name = request.form.get('team_name')
        team_lead = request.form.get('team_lead')
        member_name = request.form.get('member_name')
        member_email = request.form.get('member_email')
        member_id = request.form.get('member_id')
        profile_picture = request.files.get('profile_picture')

        # Save the profile picture
        profile_picture_filename = None
        if profile_picture and profile_picture.filename != '':
            profile_picture_filename = os.path.join(
                app.config['UPLOAD_FOLDER'], profile_picture.filename
            )
            profile_picture.save(profile_picture_filename)

        # Add data to the organization list
        organizations.append({
            'name': org_name,
            'location': org_location,
            'teams': [
                {
                    'name': team_name,
                    'lead': team_lead,
                    'members': [
                        {
                            'name': member_name,
                            'email': member_email,
                            'id': member_id,
                            'profile_picture': profile_picture_filename,
                            'status': 'Image Uploaded' if profile_picture else 'Pending'
                        }
                    ]
                }
            ]
        })

        # Redirect to the dashboard
        return redirect(url_for('dashboard'))

    # Render the registration page on GET request
    return render_template('register.html')

# Route for the dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', organizations=organizations)

if __name__ == '__main__':
    app.run(debug=True)
