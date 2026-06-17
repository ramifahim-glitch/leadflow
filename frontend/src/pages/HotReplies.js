import React,{useEffect,useState}from"react";
import{hotReplies}from"../lib/api";
const card={background:"#fff",border:"0.5px solid #e5e5e5",borderRadius:12,padding:"1rem 1.25rem",marginBottom:"0.75rem"};
export default function HotReplies(){
const[replies,setReplies]=useState([]);
useEffect(()=>{hotReplies().then(setReplies).catch(console.error);},[]);
return(<div><h2 style={{fontSize:18,fontWeight:500}}>Hot replies</h2><p style={{fontSize:13,color:"#666",marginBottom:"1rem"}}>{replies.length} leads need a follow-up.</p>{replies.map((r,i)=>(<div key={i} style={card}><div style={{fontSize:14,fontWeight:500}}>{r~irst_name} {r.last_name} - {r.company}</div><div style={{fontSize:12,color:"#666",marginTop:4}}>{r.reply_text}</div></div>))}{replies.length===0&&<p style={{fontSize:13,color:"#999"}}>No hot replies right now.</p>}</div>);}
