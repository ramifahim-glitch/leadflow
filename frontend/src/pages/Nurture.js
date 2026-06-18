import React, { useEffect, useState } from "react";
import { getNurtureTracks, getBranchingRules } from "../lib/api";

const card = {
  background: "#fff",
  border: "0.5px solid #e5e5e5",
  borderRadius: 12,
  padding: "1rem 1.25rem",
  marginBottom: "0.75rem",
};

export default function Nurture() {
  const [tracks, setTracks] = useState([]);
  const [rules, setRules] = useState([]);

  useEffect(() => {
    getNurtureTracks().then(setTracks).catch(console.error);
    getBranchingRules().then(setRules).catch(console.error);
  }, []);

  return (
    <div>
      <h2 style={{ fontSize: 18, fontWeight: 500 }}>Nurture & Sequences</h2>
      <div style={card}>
        <div style={{ fontSize: 13, fontWeight: 500, marginBottom: 8 }}>Nurture tracks</div>
        {tracks.map((t, i) => (
          <div key={i} style={{ fontSize: 13, padding: "6px 0", borderBottom: "0.5px solid #f0f0f0" }}>
            {t.name} — {t.track_type}
          </div>
        ))}
      </div>
      <div style={card}>
        <div style={{ fontSize: 13, fontWeight: 500, marginBottom: 8 }}>Branching rules</div>
        {rules.map((r, i) => (
          <div key={i} style={{ fontSize: 12, padding: "6px 0", borderBottom: "0.5px solid #f0f0f0" }}>
            {r.trigger_event} → {r.action}
          </div>
        ))}
      </div>
    </div>
  );
}
