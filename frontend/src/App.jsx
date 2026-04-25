import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [form, setForm] = useState({
    name: "",
    aadhaar: "",
    pan: "",
  });

  const [files, setFiles] = useState({
    aadhaar: null,
    pan: null,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleFile = (e) => {
    setFiles({ ...files, [e.target.name]: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setResult(null);

    const data = new FormData();
    data.append("name", form.name);
    data.append("aadhaar_number", form.aadhaar);
    data.append("pan_number", form.pan);
    data.append("aadhaar_file", files.aadhaar);
    data.append("pan_file", files.pan);

    try {
      const res = await axios.post(
        `${import.meta.env.VITE_API_URL}/api/validate`,
        data
      );
      setResult(res.data);
    } catch {
      alert("API Error");
    }

    setLoading(false);
  };

  return (
    <div className="page">
      <div className="card">
        <h1>Identity Verification</h1>

        <form onSubmit={handleSubmit}>
          <input name="name" placeholder="Full Name" onChange={handleChange} />
          <input name="aadhaar" placeholder="Aadhaar Number" onChange={handleChange} />
          <input name="pan" placeholder="PAN Number" onChange={handleChange} />

          <div className="upload-section">
            <label className="upload-box">
              <p>Aadhaar Document</p>
              <span>{files.aadhaar ? files.aadhaar.name : "Upload PDF/Image"}</span>
              <input type="file" name="aadhaar" onChange={handleFile} />
            </label>

            <label className="upload-box pan">
              <p>PAN Document</p>
              <span>{files.pan ? files.pan.name : "Upload PDF/Image"}</span>
              <input type="file" name="pan" onChange={handleFile} />
            </label>
          </div>

          <button>{loading ? "Verifying..." : "Verify Identity"}</button>
        </form>

        {/* 🔥 RESULT UI */}
        {result && (
          <div className="result-container">

            {/* ❌ ISSUES */}
            {result.errors.length > 0 && (
              <div className="result-box failed">
                <h3>Verification Issues</h3>
                <ul>
                  {result.errors.map((e, i) => (
                    <li key={i}>{e}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* ✅ VERIFIED */}
            {result.success.length > 0 && (
              <div className="result-box success">
                <h3>Verified</h3>
                <ul>
                  {result.success.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>
              </div>
            )}

          </div>
        )}
      </div>
    </div>
  );
}

export default App;