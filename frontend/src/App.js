import React from "react";
import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Brain from "./pages/Brain";
import Campaigns from "./pages/Campaigns";
import Leads from "./pages/Leads";
import Inbox from "./pages/Inbox";
import Connectors from "./pages/Connectors";
import HotReplies from "./pages/HotReplies";
import Nurture from "./pages/Nurture";

const NAV = [
  { to: "/", label: "Dashboard" },
  { to: "/brain", label: "AI Brain" },
  { to: "/campaigns", label: "Campaigns" },
  { to: "/leads", label: "Leads" },
  { to: "/nurture", label: "Nurture" },
  { to: "/inbox", label: "Inboxes" },
  { to: "/hot", label: "Hot replies" },
  { to: "/connectors", label: "Connectors" },
];

function navLinkStyle(isActive) {
  return {
    display: "block",
    padding: "8px 1rem",
    fontSize: 13,
    textDecoration: "none",
    color: isActive ? "#534AB7" : "#666",
    fontWeight: isActive ? 500 : 400,
  };
}

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ display: "flex", fontFamily: "system-ui, sans-serif" }}>
        <aside
          style={{
            width: 200,
            minHeight: "100vh",
            borderRight: "0.5px solid #e5e5e5",
            padding: "1.5rem 0",
            background: "#fafafa",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <div style={{ padding: "0 1rem 1rem", fontSize: 15, fontWeight: 600 }}>
            LeadFlow
          </div>
          {NAV.map((n) => (
            <NavLink key={n.to} to={n.to} style={({ isActive }) => navLinkStyle(isActive)}>
              {n.label}
            </NavLink>
          ))}
        </aside>
        <main style={{ flex: 1, padding: "1.5rem 2rem" }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/brain" element={<Brain />} />
            <Route path="/campaigns" element={<Campaigns />} />
            <Route path="/leads" element={<Leads />} />
            <Route path="/nurture" element={<Nurture />} />
            <Route path="/inbox" element={<Inbox />} />
            <Route path="/hot" element={<HotReplies />} />
            <Route path="/connectors" element={<Connectors />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
