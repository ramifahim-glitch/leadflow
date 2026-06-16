import React,{useEffect,useState}from"react";
import{connectorStatus,createInboxes}from"../lib/api";
const THEME=[{key:"clay",label:"Clay",role:"Enrichment + AI"},{key:"maildoso",label:"Maildoso",role:"Domains + inboxes"},{key:"instantly",label:"Instantly.ai",role:"Sending"},{key:"apollo",label:"Apollo.io",role:"Lead sourcing"},{key:"anthropic",label:"Claude API",role:"AI reasoning"},{key:"supabase",label:"Supabase",role:"Database"}];
export default function Connectors(){
const[status,setStatus]=useState({});
useEffect(()=>{connectorStatus().then(r=>setStatus(r.connectors||{})).catch(console.error);},[]);
return(<div><h2 style={{fontSize:18,fontWeight:500}}>Connectors</h2><div style={{background:"#fff",border:"0.5px solid #e5e5e5",borderRadius:12,padding:"1rem 1.25rem"}}>{THEME.map((c,i)=>(<div key={c.key} style={{display:"flex",alignItems:"center",gap:12,padding:"8px 0",borderBottom:i<THEME.length-1?"0.5px solid #f0f0f0":"none"}}><div style={{flex:1}}><div style={{fontSize:13,fontWeight:500}}>{c.label}</div><div style={{fontSize:11,color:"#888"}}>{c.role}</div></div><span style={{padding:"2px 10px",borderRadius:999,fontSize:11,fontWeight:500,whiteSpace:"nowrap",background:status[c.key]?"#E1F5EE":"#FCEBEB",color:status[c.key]?"#085041":"#791F1F"}}>{status[c.key]?"Connected":"Missing key"}</span></div>))}</div></div>);}
