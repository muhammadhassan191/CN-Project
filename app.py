from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['uploaded_images'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return redirect(url_for('home')) 


    name = request.form.get('name')
    birthdate = request.form.get('birthdate')
    cnic_type = request.form.get('cnic_type')
    address = request.form.get('address')
    file = request.files.get('image')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['uploaded_images'], filename))
    else:
        flash('Invalid image file. Only PNG, JPG, JPEG, and GIF are allowed.', 'error')
        return redirect(url_for('home'))

    if not birthdate:
        flash('Birthdate is required!', 'error')
        return redirect(url_for('home'))

    birthdate_obj = datetime.strptime(birthdate, '%Y-%m-%d')
    age = (datetime.now() - birthdate_obj).days // 365

    if age < 18:
        flash('You must be at least 18 years old to register for a CNIC.', 'error')
        return redirect(url_for('home'))

    return render_template('cnic_detail.html', name=name, birthdate=birthdate,
                           cnic_type=cnic_type, address=address, image=filename)

if __name__ == '__main__':
    app.run(debug=True)
