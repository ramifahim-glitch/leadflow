import React,{useEffect,useState}from"react";
import{todayReport,recentActivity}from"../lib/api";
const card={background:"#fff",border:"0.5px solid #e5e5e5",borderRadius:12,padding:"1rem 1.25rem",marginBottom:"1rem"};
const statCard={fleyê'à1,background:"#fff",border:"0.5px solid #e5e5e5",borderRadius:12,padding:"1rem"};
export default function Dashboard(){
const[report,setReport]=useState(null);
const[activity,setActivity]=useState([]);
useEffect(()=>{todayReport().then(setReport).catch(console.error);recentActivity().then(setActivity).catch(console.error);},[]);
return(<div><h2 style={{fontSize:18,fontWeight:500,marginBottom:"1.25rem"}}>Dashboard</h2><div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:12,marginBottom:"1.5rem"}}>{[
[Leads sourced",report?.leads_sourced||0],
[Emails sent",report?.emails_sent||0],
[Replies",report?.replies||0],
[Hot replies",report?.hot_replies||0]
].map(([label,val],i)=>(<div key={i} style={statCard}><div style={{fontSize:24,fontWeight:600,color:"#534AB7"}}>{val}</div><div style={{fontSize:12,color:"#888"}}>{label}</div></div>))}</div><div style={card}><div style={{fontSize:13,fontWeight:500,marginBottom:"0.75rem"}}>Recent activity</div>{activity.slice(0,8).map((a,i)=>(<div key={i} style={{fontSize:12,color:"#444",padding:"6px 0",borderBottom:"0.5px solid #f0f0f0"}}>{a.description||JSON.stringify(a)}</div>))}{activity.length===0&&<p style={{fontSize:12,color:"#999"}}>No activity yet.</p>}</div></div>);}
