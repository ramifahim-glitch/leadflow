import React,{useEffect,useState}from"react";
import{getCampaigns,createCampaign,pauseCampaign,activateCampaign}from"../lib/api";
const card={background:"#fff",border:"0.5px solid #e5e5e5",borderRadius:12,padding:"1rem 1.25rem",marginBottom:"0.75rem"};
export default function Campaigns(){
const[campaigns,setCampaigns]=useState([]);
useEffect(()=>{getCampaigns().then(setCampaigns).catch(console.error);},[]);
async function toggle(c){const u=c.status==="active"?await pauseCampaign(c.id):await activateCampaign(c.id);setCampaigns(p => p.map(x=>x.id===c.id?u:x));}
return(<div><h2 style={{fontSize:18,fontWeight:500}}>Campaigns</h2>{campaigns.map(c=>(<div key={c.id} style={card}><div style={{fontSize:14,fontWeight:500}}>{c.name}</div><div style={{fontSize:11,color:"#888"}}>{c.status}</div><button onClick={()=>toggle(c)} style={{marginTop:8,padding:"5px 12px",fontSize:12,borderRadius:6,cursor:"pointer",border:"0.5px solid #534AB7",background:"transparent",color:"#534AB7"}}>{c.status==="active"?"Pause":"Activate"}</button></div>))}</div>);}
