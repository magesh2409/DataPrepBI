from flask import Flask , request  , jsonify , send_from_directory
from flask_cors import CORS
import pandas as pd
from DataPrepBI import assign_datatype , find_missing_percentage , replace_with_mean , RandomForest , visualize_columns
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

data_files = 'data_files'

app.config['UPLOAD_FOLDER'] = data_files

os.makedirs(data_files , exist_ok=True)

@app.route('/')
def home_page():
    return 'This is Home Page'

@app.route('/files/upload')
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

    #perform operations
    data = assign_datatype(df)
    data = find_missing_percentage(data)
    data = replace_with_mean(data)
    data = RandomForest(data)
    visualize_columns(data)


    #save cleaned file
    cleaned_file_name = filename.rsplit('.', 1)[0] + '_cleaned.csv'
    cleaned_file_path = os.path.join(app.config['UPLOAD_FOLDER'] , cleaned_file_name)
    data.to_csv(cleaned_file_path , index=False)
    return jsonify(
        {
            'filename': cleaned_file_name
        }
    )

@app.route('/download/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'] , name , as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True , port=5000)







