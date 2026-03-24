import React, { useState } from "react";

function App() {
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;
const APP_API_KEY = process.env.REACT_APP_API_KEY;

const [reconcileInput, setReconcileInput] = useState(`{
  "patient_context": {
    "age": 67,
    "conditions": ["Type 2 Diabetes", "Hypertension"],
    "recent_labs": {"eGFR": 45}
  },
  "sources": [
    {
      "system": "Hospital EHR",
      "medication": "Metformin 1000mg twice daily",
      "last_updated": "2024-10-15",
      "source_reliability": "high"
    },
    {
      "system": "Primary Care",
      "medication": "Metformin 500mg twice daily",
      "last_updated": "2025-01-20",
      "source_reliability": "high"
    },
    {
      "system": "Pharmacy",
      "medication": "Metformin 1000mg daily",
      "last_filled": "2025-01-25",
      "source_reliability": "medium"
    }
  ]
}`);
  const [reconcileResult, setReconcileResult] = useState(null);
  const [decision, setDecision] = useState("");

const [validateInput, setValidateInput] = useState(`{
  "demographics": {
    "name": "John Doe",
    "dob": "1955-03-15",
    "gender": "M"
  },
  "medications": ["Metformin 500mg", "Lisinopril 10mg"],
  "allergies": [],
  "conditions": ["Type 2 Diabetes"],
  "vital_signs": {
    "blood_pressure": "340/180",
    "heart_rate": 72
  },
  "last_updated": "2024-06-15"
}`);
  const [validateResult, setValidateResult] = useState(null);

  const callReconcile = async () => {
  try {
    JSON.parse(reconcileInput); // validate JSON

    const res = await fetch(`${API_BASE_URL}/api/reconcile/medication`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "x-api-key": APP_API_KEY
      },
      body: reconcileInput,
    });

    const data = await res.json();
    setReconcileResult(data);
    setDecision("");
  } catch (err) {
    console.error("API error:", err);
    alert("Invalid JSON input");
  }
};

const callValidate = async () => {
  try {
    JSON.parse(validateInput); // validate JSON

    const res = await fetch(`${API_BASE_URL}/api/validate/data-quality`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "x-api-key": APP_API_KEY
      },
      body: validateInput,
    });

    const data = await res.json();
    setValidateResult(data);
    setDecision("");
  } catch (err) {
    console.error("API error:", err);
    alert("Invalid JSON input");
  }
};

  const getColor = (score) => {
    if (score >= 80) return "green";
    if (score >= 60) return "orange";
    return "red";
  };

  return (
    <div style={{ padding: 30,
                  fontFamily: "Arial",
                  maxWidth: "900px",
                  margin: "auto" 
                  }}>
    <h1 style={{ marginBottom: 30 }}>EHR Reconciliation & Data Quality Dashboard</h1>

      {/* ================= RECONCILIATION ================= */}
      <h2 style={{ marginTop: 30 }}>Medication Reconciliation</h2>

      <textarea
        rows={10}
        style={{ width: "100%", marginBottom: 10}}
        value={reconcileInput}
        onChange={(e) => setReconcileInput(e.target.value)}
      />

      <br />
      <button style={{
        padding: "8px 14px",
        backgroundColor: "#2c7be5",
        color: "white",
        border: "none",
        borderRadius: 5,
        cursor: "pointer"
      }} onClick={callReconcile}>Run Reconciliation</button>

      {reconcileResult && (
        <div style={{ 
              border: "1px solid #ddd",
              borderRadius: 8,
              padding: 20,
              marginTop: 20,
              backgroundColor: "#fafafa"
              }}>
          <h3>Result</h3>

          <p>
            <b>Medication:</b> {reconcileResult.reconciled_medication}
          </p>

          <p>
            <b>Confidence:</b>{" "}
            <span style={{ color: getColor(reconcileResult.confidence_score * 100) }}>
              {(reconcileResult.confidence_score * 100).toFixed(0)}%
            </span>
          </p>

          <p>
            <b>Reasoning:</b> {reconcileResult.reasoning}
          </p>

          <p><b>Recommended Actions:</b></p>
          <ul>
            {reconcileResult.recommended_actions.map((a, i) => (
              <li key={i}>{a}</li>
            ))}
          </ul>

          {decision === "Approved" && (
            <p style={{ color: "green" }}>
              ✔ Clinician accepted AI recommendation
            </p>
          )}

          {decision === "Rejected" && (
            <p style={{ color: "red" }}>
              ✖ Clinician rejected AI recommendation
            </p>
          )}
          <button 
            onClick={() => setDecision("Approved")}
            style={{ backgroundColor: "green", color: "white", marginRight: 10 }}>
            Approve
          </button>

          <button 
            onClick={() => setDecision("Rejected")} 
            style={{ backgroundColor: "red", color: "white" }}>
            Reject
          </button>
        </div>
      )}

      <hr style={{ margin: "30px 0" }} />

      {/* ================= DATA QUALITY ================= */}
      <h2 style={{ marginTop: 40 }}>Data Quality Assessment</h2>

      <textarea
        rows={10}
        style={{ width: "100%", marginBottom: 10}}
        value={validateInput}
        onChange={(e) => setValidateInput(e.target.value)}
      />

      <br />
      <button style={{
        padding: "8px 14px",
        backgroundColor: "#2c7be5",
        color: "white",
        border: "none",
        borderRadius: 5,
        cursor: "pointer"
      }} onClick={callValidate}>Run Validation</button>

      {validateResult && (
        <div style={{
              border: "1px solid #ddd",
              borderRadius: 8,
              padding: 20,
              marginTop: 20,
              backgroundColor: "#fafafa"
              }}>
          <h3>
            Overall Score:{" "}
            <span style={{ color: getColor(validateResult.overall_score) }}>
              {validateResult.overall_score}
            </span>
          </h3>

          <h4>Breakdown</h4>
          <ul>
            {Object.entries(validateResult.breakdown).map(([k, v]) => (
              <li key={k}>
                {k}:
                <span style={{
                  color: getColor(v),
                  fontWeight: "bold",
                  marginLeft: 5
                }}>{v}</span>
              </li>
            ))}
          </ul>

          <h4>Issues Detected</h4>
          <ul>
            {validateResult.issues_detected.map((issue, idx) => (
              <li key={idx}>
                <b>{issue.field}</b>: {issue.issue}
                <span style={{
                  color: issue.severity === "high" ? "red" : 
                  issue.severity === "medium" ? "orange" : "green",
                  marginLeft: 8,
                  fontWeight: "bold"
                }}>
                 ({issue.severity})
                </span>
              </li>
            ))}
          </ul>

          <h4 style={{ marginTop: 20 }}>AI Clinical Summary</h4>
          <p style={{ lineHeight: 1.6 }}>
            {validateResult.llm_summary}</p>
        </div>
      )}
    </div>
  );
}

export default App;