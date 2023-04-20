from flask import Flask, request, render_template, redirect, url_for, jsonify, flash, send_from_directory
import os
from flaskext.mysql import MySQL
from datetime import datetime
import csv
from jinja2 import Markup

USERS = {'user': 'password'}
Data_Pozos = []
Data_Pozos2 =[]
Data_Pozos3 =[]
app = Flask(__name__, static_folder='static')
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'JPG'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/static/uploads/<nombreFoto>')
def uploads(nombreFoto):

    return send_from_directory(app.config['UPLOAD_FOLDER'],nombreFoto)

@app.route('/index', methods=['GET', 'POST'])
def index():
    global Data_Pozos2
    global Data_Year
    global Data_Location
    file_path = "form_data.csv"
    if not os.path.exists(file_path):
    # Create the file
        open(file_path, 'w').close() 
    Data_Pozos = [] # read the data from form_data.csv and store it in a list
    Data_Pozos2 = []
    with open(file_path) as f:
        # skip the header row
        for line in f:
            pozo = line.strip().split(',')[1]
            Data_Pozos.append(pozo)
    with open(file_path) as f:
        # skip the header row
        for line in f:
            pozo2 = line.strip().split(',')
            pozo2[1]=line.strip().split(',')[1].split("-")[0]
            Data_Pozos2.append(pozo2)
    Data_Year = [] # extract the year information from form_data.csv and store it in a list
    Data_Location=[]
    with open(file_path) as f: 
        for line in f:
            year = line.strip().split(',')[1].split("-")[0]
            location=line.strip().split(',')[3]
            Data_Year.append(year)
            Data_Location.append(location)
    
    unique_years = list(set(Data_Year))
    unique_years = sorted(unique_years)
    unique_location = list(set(Data_Location))
    unique_location = sorted(unique_location, key=lambda x: int(x.split(" ")[1]))
    return render_template('index.html', Data_Pozos2=Data_Pozos2, Data_Year=unique_years
    , Data_Location=unique_location)

@app.route('/logeado', methods=['GET', 'POST'])
def logeado():
    global Data_Pozos2
    global Data_Year
    global Data_Location
    global Search

    Search=1
    file_path = "form_data.csv"
    if not os.path.exists(file_path):
    # Create the file
        open(file_path, 'w').close() 
    Data_Pozos = [] # read the data from form_data.csv and store it in a list
    Data_Pozos2 = []
    with open(file_path) as f:
        # skip the header row
        for line in f:
            pozo = line.strip().split(',')[1]
            Data_Pozos.append(pozo)
    with open(file_path) as f:
        # skip the header row
        for line in f:
            pozo2 = line.strip().split(',')
            pozo2[1]=line.strip().split(',')[1].split("-")[0]
            Data_Pozos2.append(pozo2)
    Data_Year = [] # extract the year information from form_data.csv and store it in a list
    Data_Location=[]
    with open(file_path) as f: 
        for line in f:
            year = line.strip().split(',')[1].split("-")[0]
            location=line.strip().split(',')[3]
            Data_Year.append(year)
            Data_Location.append(location)
    
    unique_years = list(set(Data_Year))
    unique_years = sorted(unique_years)
    unique_location = list(set(Data_Location))
    unique_location = sorted(unique_location, key=lambda x: int(x.split(" ")[1]))
    return render_template('logeado.html', Data_Pozos2=Data_Pozos2, Data_Year=unique_years
    , Data_Location=unique_location, Search=Search)
@app.route('/login', methods=['POST'])
def login():
    username = request.form['uname']
    password = request.form['psw']
    if username in USERS and USERS[username] == password:
        return render_template('logeado.html')
    else:
        return render_template('index.html', error='Incorrect username or password')

@app.route('/create', methods=['GET', 'POST'])
def create():
    return render_template('/create.html')

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    global Data_Pozos2
    global filtered_data
    fecha_buscar=request.form['year']
    location_buscar=request.form['location']
    # print(location_buscar)
    # print(Data_Pozos2)
    filtered_data = [pozo for pozo in Data_Pozos2 if pozo[1] == fecha_buscar and location_buscar in pozo[3]]
    print(filtered_data)
    if len(filtered_data) == 0:
        return render_template('/nopozo.html')
    else:
        return render_template('buscar.html', filtered_data=filtered_data)

@app.route('/buscar2', methods=['GET', 'POST'])
def buscar2():
    global Data_Pozos2
    global filtered_data
    fecha_buscar=request.form['year2']
    location_buscar=request.form['location2']
    # print(location_buscar)
    # print(Data_Pozos2)
    filtered_data = [pozo for pozo in Data_Pozos2 if pozo[1] == fecha_buscar and location_buscar in pozo[3]]
    print(filtered_data)
    if len(filtered_data) == 0:
        return render_template('/nopozo2.html')
    else:
        return render_template('buscar2.html', filtered_data=filtered_data)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def delete_from_csv(file_path, value):
    # Create a temporary file to write the updated data to
    tmp_file_path = "tmp.csv"

    with open(file_path, "r") as csv_file, open(tmp_file_path, "w", newline="") as tmp_file:
        reader = csv.reader(csv_file)
        writer = csv.writer(tmp_file)

        # Iterate over each row in the CSV file
        for row in reader:
            # Check if the row contains the value to be deleted
            if value in row:
                continue  # Skip this row

            # Write the row to the temporary file
            writer.writerow(row)
    # Replace the original file with the temporary file
    os.remove(file_path)
    os.rename(tmp_file_path, file_path)
@app.route('/delete/<string:name>')
def delete(name):
    # Remove the desired value from the CSV file
    file_path = "form_data.csv"
    delete_from_csv(file_path, name)
     # Remove the matching images
    images_path = os.path.join(app.config['UPLOAD_FOLDER'])
    for filename in os.listdir(images_path):
        if name in filename:
            os.remove(os.path.join(images_path, filename))
    # Redirect the user to the home page
    return render_template('/eliminado.html')

@app.route('/edit/<string:name>')
def edit(name):
    # Select the desired row from the CSV file
    file_path = "form_data.csv"
    selected_row = None
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == name:
                selected_row = row
                break
    # Render the 'view.html' template with the selected row
    return render_template('/edit.html', row=selected_row)
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'txtFotoMonumento1' not in request.files:
        return redirect(url_for('create'))

    file = request.files['txtFotoMonumento1']
    file2 = request.files['txtFotoMonumento2']
    file3 = request.files['txtFotoLocacion1']
    file4 = request.files['txtFotoLocacion2']
    form_data = request.form

    file_path = 'form_data.csv'
    # Check if the file already exists
    if not os.path.exists(file_path):
        # Create the file
        open(file_path, 'w').close()
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        # Check if the well is already created
        well_created = False
        for row in reader:
            if form_data['txtNombrePozo'] == row[0]:
                well_created = True
                break
        if well_created:
            # Perform actions if the well already exists
            return render_template('/existe.html')
        else:
            # Perform actions if the well does not exist
            with open(file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
        form_data['txtNombrePozo'],
        form_data['txtFecha'],
        form_data['txtNombreCluster'],
        form_data['txtNombreFrancia'],
        form_data['txtid1'],
        form_data['txtcid1'],
        form_data['txtid2'],
        form_data['txtcid2'],
        form_data['txtid3'],
        form_data['txtcid3'],
        form_data['txtid4'],
        form_data['txtcid4'],
        form_data['txtid5'],
        form_data['txtcid5'],
        form_data['txtid6'],
        form_data['txtcid6'],
        form_data['txtid7'],
        form_data['txtcid7'],
        form_data['txtid8'],
        form_data['txtcid8'],
        form_data['txtid20'],
        form_data['txtcid20'],
        form_data['txtid41'],
        form_data['txtcid41'],
        form_data['txtid42'],
        form_data['txtcid42'],
        form_data['txtid45'],
        form_data['txtcid45'],
        form_data['txtid46'],
        form_data['txtcid46'],
        form_data['txtid104'],
        form_data['txtcid104'],
        form_data['txtid105'],
        form_data['txtcid105'],
        form_data['txtid108'],
        form_data['txtcid108'],
        form_data['txtid109'],
        form_data['txtcid109']
    ])
            # Continue with the rest of the code
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                Data_Pozos.extend(list(reader))
            if file.filename == '':
                return redirect(url_for('create'))

            if file and allowed_file(file.filename):
                name1 = request.form['txtFecha']
                date_object = datetime.strptime(name1, '%Y-%m-%d')
                year = date_object.strftime("%Y")
                name1 = year + request.form['txtNombrePozo']
                filename, file_extension = os.path.splitext(file.filename)
                new_filename = name1 + '_monumento1' + file_extension
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                existe = os.path.exists(file_path)
            if existe == False:
                file.save(file_path)

            if file2 and allowed_file(file2.filename):
        # Save the second image with a different filename
                new_filename = name1 + '_monumento2' + file_extension
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                existe = os.path.exists(file_path)
            if existe == False:
                file2.save(file_path)

            if file3 and allowed_file(file3.filename):
        # Save the third image with a different filename
                new_filename = name1 + '_locacion1' + file_extension
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                existe = os.path.exists(file_path)
            if existe == False:
                file3.save(file_path)

            if file4 and allowed_file(file4.filename):
        # Save the fourth image with a different filename
                new_filename = name1 + '_locacion2' + file_extension
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                existe = os.path.exists(file_path)
            if existe == False:
                file4.save(file_path)

    return render_template('/success.html')
    
@app.route('/edited', methods=['GET', 'POST'])
def edited():
    form_data = request.form
    name=form_data['name']
    file_path = 'form_data.csv'
    selected_row2 = None
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == name:
                selected_row2 = row
                break
    file = request.files['txtFotoMonumento1']
    file2 = request.files['txtFotoMonumento2']
    file3 = request.files['txtFotoLocacion1']
    file4 = request.files['txtFotoLocacion2']
    year = selected_row2[1][:4]
    name1 = year + selected_row2[0]
    if file and allowed_file(file.filename):
        filename, file_extension = os.path.splitext(file.filename)
        new_filename = name1 + '_monumento1' + file_extension
        file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        existe = os.path.exists(file_path2)
        file.save(file_path2)
    if file2 and allowed_file(file2.filename):
        filename, file_extension = os.path.splitext(file2.filename)
        # Save the second image with a different filename
        new_filename = name1 + '_monumento2' + file_extension
        file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        existe2 = os.path.exists(file_path2)
        file2.save(file_path2)

    if file3 and allowed_file(file3.filename):
        # Save the third image with a different filename
        filename, file_extension = os.path.splitext(file3.filename)
        new_filename = name1 + '_locacion1' + file_extension
        file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        existe3 = os.path.exists(file_path2)
        file3.save(file_path2)

    if file4 and allowed_file(file4.filename):
    # Save the fourth image with a different filename
        filename, file_extension = os.path.splitext(file4.filename)
        new_filename = name1 + '_locacion2' + file_extension
        file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        existe4 = os.path.exists(file_path2)
        file4.save(file_path2)
        
    delete_from_csv(file_path, name)
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([selected_row2[0] ,
        selected_row2[1] ,
        selected_row2[2] ,
        selected_row2[3] ,
        form_data['txtid1'],
        form_data['txtcid1'],
        form_data['txtid2'],
        form_data['txtcid2'],
        form_data['txtid3'],
        form_data['txtcid3'],
        form_data['txtid4'],
        form_data['txtcid4'],
        form_data['txtid5'],
        form_data['txtcid5'],
        form_data['txtid6'],
        form_data['txtcid6'],
        form_data['txtid7'],
        form_data['txtcid7'],
        form_data['txtid8'],
        form_data['txtcid8'],
        form_data['txtid20'],
        form_data['txtcid20'],
        form_data['txtid41'],
        form_data['txtcid41'],
        form_data['txtid42'],
        form_data['txtcid42'],
        form_data['txtid45'],
        form_data['txtcid45'],
        form_data['txtid46'],
        form_data['txtcid46'],
        form_data['txtid104'],
        form_data['txtcid104'],
        form_data['txtid105'],
        form_data['txtcid105'],
        form_data['txtid108'],
        form_data['txtcid108'],
        form_data['txtid109'],
        form_data['txtcid109']
    ])
        return render_template('/editado.html')
    
@app.route('/view/<string:name>')
def view(name):
    # Select the desired row from the CSV file
    file_path = "form_data.csv"
    selected_row = None
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == name:
                selected_row = row
                break
   # Check if the image files exist for locacion and monumento
    locacion_images = []
    monumento_images = []
    for i in range(1, 3):
        locacion_filename = row[1][:4] + row[0] + f'_locacion{i}.jpg'
        monumento_filename = row[1][:4] + row[0] + f'_monumento{i}.jpg'
        print("Locacion ruta es"+locacion_filename)
        print("Monumento ruta es"+monumento_filename)
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], locacion_filename)):
            locacion_images.append(locacion_filename)
            # print("Locacion images:", locacion_images)
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], monumento_filename)):
            monumento_images.append(monumento_filename)
            # print("monumento images:", monumento_images)
     # Add a timestamp to the image URL
    image_version = int(datetime.utcnow().timestamp())
    # Render the 'view.html' template with the selected row and image file names
    return render_template('/view.html', row=selected_row, locacion_images=locacion_images, monumento_images=monumento_images,image_version=image_version)
@app.route('/overwrite', methods=['POST'])
def overwrite():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], request.form['filename'])
    file = request.files['file']
    file.save(file_path)
    return redirect(url_for('success'))

if __name__=='__main__':
    app.run(debug=True)



