import React, { useState } from "react";
import { analyseBrain } from "../lib/api";

const card = {
  background: "#fff",
  border: "0.5px solid #e5e5e5",
  borderRadius: 12,
  padding: "1rem 1.25rem",
  marginBottom: "1rem",
};

export default function Brain() {
  const [offering, setOffering] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function analyse() {
    if (!offering.trim()) return;
    setLoading(true);
    try {
      const res = await analyseBrain({ offering });
      setResult(res);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h2 style={{ fontSize: 18, fontWeight: 500 }}>AI Brain</h2>
      <p style={{ fontSize: 13, color: "#666", marginBottom: "1rem" }}>
        Describe your services once. The AI builds your ICP, buying signals, and personalization angles.
      </p>
      <div style={card}>
        <textarea
          style={{
            width: "100%",
            fontSize: 13,
            borderRadius: 8,
            border: "0.5px solid #ddd",
            padding: "8px 10px",
            fontFamily: "inherit",
            resize: "vertical",
            minHeight: 80,
            boxSizing: "border-box",
          }}
          placeholder="Describe what you offer..."
          value={offering}
          onChange={(e) => setOffering(e.target.value)}
        />
        <button
          style={{
            marginTop: "1rem",
            padding: "8px 16px",
            fontSize: 13,
            borderRadius: 8,
            cursor: "pointer",
            border: "none",
            background: "#534AB7",
            color: "#fff",
          }}
          onClick={analyse}
          disabled={loading}
        >
          {loading ? "Analysing..." : "Analyse & generate ICPs"}
        </button>
      </div>
      {result && (
        <div style={card}>
          <div style={{ fontSize: 13, fontWeight: 500 }}>Personas</div>
          {result.personas?.map((p, i) => (
            <div key={i} style={{ padding: "6px 0", fontSize: 13, borderBottom: "0.5px solid #f0f0f0" }}>
              <strong>{p.title}</strong> — fit: {p.fit_score}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
