import React,{useEffect,useState}from"react";
import{listInboxes}from"../lib/api";
const card={background:"#fff",border:"0.5px solid #e5e5e5",borderRadius:12,padding:"1rem 1.25rem"};
export default function Inbox(){
const[inboxes,setInboxes]=useState([]);
useEffect(()=>{listInboxes().then(setInboxes).catch(console.error);},[]);
return(<div><h2 style={{fontSize:18,fontWeight:500}}>Inboxes</h2><div style={card}>{inboxes.map((b,i)=>(<div key={i} style={{display:"flex",justifyContent:"space-between",padding:"8px 0",borderBottom:i<inboxes.length-1?"0.5px solid #f0f0f0":"none"}}><span style={{fontSize:13}}>{b.email}</span><span style={{fontSize:11,color:"#888"}}>{b.status}</span></div>))}{inboxes.length===0&&<p style={{fontSize:13,color:"#999"}}>No inboxes yet. Create some from Connectors.</p>}</div></div>);}
