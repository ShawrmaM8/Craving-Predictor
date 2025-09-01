// frontend/src/App.jsx
import React, { useState, useEffect } from 'react';
import { submitReport, getPrediction } from './api';

export default function App() {
  const [anonId, setAnonId] = useState('user123');
  const [sleep, setSleep] = useState(7);
  const [stress, setStress] = useState(5);
  const [urges, setUrges] = useState([]);
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async () => {
    const report = {
      anon_id: anonId,
      date: new Date().toISOString(),
      sleep_hours: sleep,
      stress: stress,
      urges: urges,
      app_usage: {},
      notes: ''
    };
    await submitReport(report);
    fetchPrediction();
  };

  const fetchPrediction = async () => {
    const data = await getPrediction(anonId);
    setPrediction(data);
  };

  useEffect(() => {
    fetchPrediction();
    const interval = setInterval(fetchPrediction, 15000); // auto-update every 15s
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: 20, fontFamily: 'sans-serif' }}>
      <h1>Personal Urge Predictor</h1>
      <div>
        <label>Sleep Hours: </label>
        <input type="number" value={sleep} onChange={e => setSleep(Number(e.target.value))} />
      </div>
      <div>
        <label>Stress Level: </label>
        <input type="number" value={stress} onChange={e => setStress(Number(e.target.value))} />
      </div>
      <button onClick={handleSubmit}>Submit Report</button>

      {prediction && (
        <div style={{ marginTop: 20, padding: 10, border: '1px solid gray' }}>
          <h3>Prediction</h3>
          <pre>{JSON.stringify(prediction, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
