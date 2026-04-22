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

  // Professional message formatter
  const formatError = (msg) => {
    if (msg.includes("Aadhaar")) return "Aadhaar number does not match";
    if (msg.includes("PAN")) return "PAN number does not match";
    if (msg.includes("Name")) return "Name does not match document";
    if (msg.includes("not found")) return "Required data not found in document";
    return msg;
  };

  const formatSuccess = (msg) => {
    if (msg.includes("Aadhaar")) return "Aadhaar matched";
    if (msg.includes("PAN")) return "PAN matched";
    if (msg.includes("Name")) return "Name matched";
    return msg;
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
        `${process.env.REACT_APP_API_URL}/api/validate`,
        data
      );
      setResult(res.data);
    } catch (err) {
      alert("Request failed. Please check inputs or server.");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Identity Verification</h2>

        <form onSubmit={handleSubmit}>
          <input name="name" placeholder="Full Name" onChange={handleChange} />
          <input name="aadhaar" placeholder="Aadhaar Number" onChange={handleChange} />
          <input name="pan" placeholder="PAN Number" onChange={handleChange} />

          <input type="file" name="aadhaar" onChange={handleFile} />
          <input type="file" name="pan" onChange={handleFile} />

          <button disabled={loading}>
            {loading ? "Checking..." : "Verify"}
          </button>
        </form>

        {result && (
          <div className={`result ${result.status}`}>
            <h3>
              Verification Result:{" "}
              {result.status === "success" ? "Successful" : "Failed"}
            </h3>

            {result.errors.length > 0 && (
              <>
                <h4>Issues</h4>
                <ul className="error">
                  {result.errors.map((e, i) => (
                    <li key={i}>{formatError(e)}</li>
                  ))}
                </ul>
              </>
            )}

            {result.success.length > 0 && (
              <>
                <h4>Verified</h4>
                <ul className="success">
                  {result.success.map((s, i) => (
                    <li key={i}>{formatSuccess(s)}</li>
                  ))}
                </ul>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;