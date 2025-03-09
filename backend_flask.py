from flask import Flask , request , send_file , jsonify
from flask_cors import CORS
import pandas as pd
from DataPrepBI import assign_datatype , find_missing_percentage , replace_with_mean , RandomForest , visualize_columns
import os

app = Flask(__name__)
CORS(app)
base_url = 'http://localhost:5173'

uploaded_files = 'uploads'
processed_files = 'processed'

os.makedirs(uploaded_files , exist_ok=True)
os.makedirs(processed_files , exist_ok=True)



@app.route('/')
def home_page():
    return 'This is Home Page'

@app.route(f'{base_url}/upload'  , methods=['POST'])
def clean_file():

    if 'file' not in request.files:
        return jsonify({
            'error' : 'No File is Uploaded'
        }) , 400


    file = request.files['file']

    if file.filename == '':
        return jsonify({
            'error' : 'File Name is Emprty'
        }) , 400


    file_path = os.path.join(uploaded_files , file.filename)
    file.save(file_path)
    df = pd.read_csv(file)

    #perform operations
    data = assign_datatype(df)
    data = find_missing_percentage(data)
    data = replace_with_mean(data)
    data = RandomForest(data)
    data = visualize_columns(data)


    #save cleaned file
    cleaned_file_name = file.filename + '_cleaned'
    cleaned_file_path = os.path.join(processed_files , cleaned_file_name)
    data.to_csv(cleaned_file_path , index=False)








