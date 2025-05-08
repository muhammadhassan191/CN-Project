from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Set up file upload folder
UPLOAD_FOLDER = 'static/uploaded_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route displaying the CNIC registration form
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        birthdate = request.form['birthdate']
        cnic_type = request.form['cnic_type']
        address = request.form['address']
        
        # Handle file upload
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Invalid image file. Only PNG, JPG, JPEG, and GIF are allowed.', 'error')
            return redirect(url_for('home'))

        # Validate birthdate and check age
        if not birthdate:
            flash('Birthdate is required!', 'error')
            return redirect(url_for('home'))

        birthdate_obj = datetime.strptime(birthdate, '%Y-%m-%d')
        age = (datetime.now() - birthdate_obj).days // 365

        if age < 18:
            flash('You must be at least 18 years old to register for a CNIC.', 'error')
            return redirect(url_for('home'))

        # After form submission, show the CNIC details
        return render_template('cnic_detail.html', name=name, birthdate=birthdate, 
                               cnic_type=cnic_type, address=address, image=filename)

if __name__ == '__main__':
    app.run(debug=True)
