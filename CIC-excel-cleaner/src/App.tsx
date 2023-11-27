import './App.css'
import React, { useState, ChangeEvent } from 'react';
import axios from 'axios';

const App: React.FC = () => {
  const [inputFile, setInputFile] = useState<File | null>(null);
  const [outputFile, setOutputFile] = useState<File | null>(null);

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

  const handleClean = () => {
    if (!inputFile || !outputFile) {
      console.error('Please select both input and output CSV files.');
      return;
    }

    const formData = new FormData();
    formData.append('input_file_path', inputFile);
    formData.append('output_file_path', outputFile);

    axios.post('http://localhost:5000/clean', formData)
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  };


  return (
<div>
      <h1>CSV Cleaner</h1>
      <div>
        <label>Input CSV file:</label>
        <input type="file" accept=".csv" onChange={handleInputChange} />
      </div>
      <div>
        <label>Output CSV file:</label>
        <input type="file" accept=".csv" onChange={handleOutputChange} />
      </div>
      <button onClick={handleClean}>Clean CSV</button>
    </div>
  )
}

export default App
