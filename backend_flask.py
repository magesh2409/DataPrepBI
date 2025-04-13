import flask_cors
from flask import Flask , request  , jsonify , send_from_directory
from flask_cors import CORS , cross_origin
import pandas as pd
from DataPrepBI import assign_datatype , find_missing_percentage , replace_with_mean , RandomForest , visualize_columns
import os
from werkzeug.utils import secure_filename
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger('flask_cors').level = logging.DEBUG
logger = logging.getLogger('HELLO WORLD')

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

data_files = 'data_files'

app.config['UPLOAD_FOLDER'] = data_files

os.makedirs(data_files , exist_ok=True)


@app.route('/' , methods=['GET'])
def home_page():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api' , methods=['GET'])
def home_page_():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/users')
def show_users():
    return jsonify({
        'name' : 'Magesh' ,
        'email' : 'magesh@gmail..com'
    })


@app.route('/api/files/upload', methods=['POST'])
@cross_origin()
def clean_file():

    if 'file' not in request.files:
        return jsonify({
            'error' : 'No File is Uploaded'
        }) , 400


    file = request.files['file']

    if file.filename == '':
        return jsonify({
            'error' : 'File Name is Empty'
        }) , 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'] , filename)
    file.save(file_path)
    df = pd.read_csv(file_path)
    print(df.head())

    #perform operations
    data = assign_datatype(df)
    data = find_missing_percentage(data)
    data = replace_with_mean(data)
    data = RandomForest(data)
    plot_filename = visualize_columns(data)


    #save cleaned file
    cleaned_file_name = filename.rsplit('.', 1)[0] + '_cleaned.csv'
    cleaned_file_path = os.path.join(app.config['UPLOAD_FOLDER'] , cleaned_file_name)
    data.to_csv(cleaned_file_path , index=False)
    return jsonify(
        {
            'filename': cleaned_file_name,
            'plot_filename' : plot_filename
        }
    )

@app.route('/api/download/<name>', methods=['GET'])
@cross_origin()
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'] , name , as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001)







