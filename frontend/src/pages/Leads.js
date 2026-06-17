import React, { useEffect, useState } from "react";
import { getLeads } from "../lib/api";
const card = { background: "#fff", border: "0.5px solid #e5e5e5", borderRadius: 12, padding: "1rem 1.25rem" };
export default function Leads() {
  const [leads, setLeads] = useState([]);
  useEffect(() => { getLeads().then(r => setLeads(r.leads || r)).catch(console.error); }, []);
  return (
    <div>
      <h2 style={{ fontSize: 18, fontWeight: 500 }}>Leads</h2>
      <p style={{ fontSize: 13, color: "#666", marginBottom: "1rem" }}>{leads.length} leads total</p>
      <div style={card}>
        {leads.map((l, i) => (
          <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: i < leads.length - 1 ? "0.5px solid #f0f0f0" : "none" }}>
            <span style={{ fontSize: 13 }}>{l.first_name} {l.last_name} — {l.company}</span>
            <span style={{ fontSize: 11, color: "#888" }}>{l.status}</span>
          </div>
        ))}
        {leads.length === 0 && <p style={{ fontSize: 13, color: "#999" }}>No leads yet.</p>}
      </div>
    </div>
  );
}
