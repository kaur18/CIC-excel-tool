from flask import Flask, request, jsonify
from flask_cors import CORS  
import pandas as pd
from os import write
import numpy as np
import csv
from scipy import stats
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/set_upload_folder', methods=['POST'])
def set_upload_folder():
    global UPLOAD_FOLDER

    try:
        data = request.json
        new_upload_folder = data.get('upload_folder')

        UPLOAD_FOLDER = new_upload_folder
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        return jsonify({'status': 'success', 'message': f'Upload folder set to {UPLOAD_FOLDER}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/clean', methods=['POST'])
def clean_csv():
    try:
        print(request.files)
        if 'input_file' not in request.files or 'output_file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part'})

        input_file = request.files['input_file']
        output_file = request.files['output_file']

        # Check if the file names are empty
        if input_file.filename == '' or output_file.filename == '':
            return jsonify({'status': 'error', 'message': 'Invalid file names'})

        # Check if the file extensions are allowed
        if not allowed_file(input_file.filename) or not allowed_file(output_file.filename):
            return jsonify({'status': 'error', 'message': 'Invalid file extension'})

        # Save the files to the server
        input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], input_file.filename)
        output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], output_file.filename)

        print(f"Input file path: {input_file_path}")
        print(f"Output file path: {output_file_path}")

        if not os.path.exists(input_file_path) or not os.path.exists(output_file_path):
            return jsonify({'status': 'error', 'message': 'Input or output file does not exist'})

        input_file.save(input_file_path)
        output_file.save(output_file_path)
        df = pd.read_csv(input_file_path)
        deleted = ["ALPHABRODER", "BULLET LINE LLC", "CIC - ALPHARETTA", "D. PEYSER/M V SPORT", "DAVID PEYSER - ALABAMA", "ECOMPANYSTORE.COM", "ECOMPANYSTORE.COM-OFFICE", "HUETONE IMPRINTS,INC.", "LC MARKETING", "PRIME RESOURCES OUTBOUND"]

        df_filtered = df.drop(df[df["Shipper Name"].isin(deleted)].index)
        for index,row in df_filtered.iterrows():
            row["Reference Number(s)"] = str(row["Reference Number(s)"])
            row["Reference Number(s)"] = row["Reference Number(s)"].replace("PONUM","")
            row["Reference Number(s)"] = row["Reference Number(s)"].replace("PO#","")
            numbers = row["Reference Number(s)"].split("|")
            row["Reference Number(s)"] = None
            for j in numbers:
                if j[0] == "4" and len(j) == 6:
                    row["Reference Number(s)"] = j
                    break
        df_filtered.dropna(subset=["Reference Number(s)"], inplace=True)
        with open(output_file_path, "w",newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["PONumber","DateShipped","TrackingNumber"])
            for index,row in df_filtered.iterrows():
                writer.writerow([row["Reference Number(s)"], row["Manifest Date"], row["Tracking Number"]])
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)