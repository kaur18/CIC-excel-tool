import './App.css'
import React, { useState, ChangeEvent } from 'react';
import axios from 'axios';

const App: React.FC = () => {
  const [inputFile, setInputFile] = useState<File | null>(null);
  const [outputFile, setOutputFile] = useState<File | null>(null);
  const [uploadFolderPath, setUploadFolderPath] = useState<string>('');

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setInputFile(e.target.files[0]);
    }
  };

  const handleOutputChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setOutputFile(e.target.files[0]);
    }
  };

  const handleUploadFolderChange = (e: ChangeEvent<HTMLInputElement>) => {
    setUploadFolderPath(e.target.value); // Update the state when the text field changes
  };

  const handleClean = () => {
    if (!inputFile || !outputFile) {
      console.error('Please select both input and output CSV files.');
      return;
    }
    console.log("Cleaning CSV...")

    const formData = new FormData();
    formData.append('input_file', inputFile);
    formData.append('output_file', outputFile);
    axios.post('http://localhost:5000/set_upload_folder', { upload_folder: uploadFolderPath })
      .then(response => {
        console.log('Upload folder set:', response.data);
      axios.post('http://localhost:5000/clean', formData)
        .then(response => {
          console.log("Cleaning Successful:", response.data);
        })
        .catch(error => {
          console.error('Cleaning error:', error);
        });
      })
      .catch(error => {
        console.error('Upload folder set error:', error);
      });
  };


  return (
<div>
      <h1>CSV Cleaner</h1>
      <br />
      <br />
      <div>
        <label>Enter Upload Folder Path: </label>
        <input type="text" value={uploadFolderPath} onChange={handleUploadFolderChange} />
      </div>
      <br />
      <div>
        <label>Input CSV file: </label>
        <input type="file" accept=".csv" onChange={handleInputChange} />
      </div>
      <br />
      <div>
        <label>Output CSV file: </label>
        <input type="file" accept=".csv" onChange={handleOutputChange} />
      </div>
      <br />
      <button onClick={handleClean}>Clean CSV</button>
    </div>
  );
};

export default App;
