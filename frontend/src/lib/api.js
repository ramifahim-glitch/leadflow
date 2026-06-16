const BASE = process.env.REACT_APP_API_URL || "http://localhost:5000/api";
async function req(path, options={}) {
  const res = await fetch(`${BASE}${path}`, {headers:{"Content-Type":"application/json"},...options,body:options.body?JSON.stringify(options.body):undefined});
  if(!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}
export const analyseBrain=d=>req("/brain/analyse",{method:"POST",body:d});
export const getCampaigns=()=>req("/campaigns/");
export const createCampaign=d=>req("/campaigns/",{method:"POST",body:d});
export const pauseCampaign=id=>req(`/campaigns/${id}/pause`,{method:"POST"});
export const activateCampaign=id=>req(`/campaigns/${id}/activate`,{method:"POST"});
export const getLeads=(p={})=>req("/leads/?"+new URLSearchParams(p));
export const enrichLead=id=>req(`/leads/enrick/${id}`,{method:"POST"});
export const todayReport=()=>req("/reports/today");
export const recentActivity=()=>req("/reports/activity");
export const hotReplies=()=>req("/reports/hot-replies");
export const connectorStatus=()=>req("/connectors/status");
export const listInboxes=()=>req("/connectors/inboxes");
export const createInboxes=d=>req("/connectors/maildoso/create",{method:"POST",body:d});
export const personaliseMsg=d=>req("/brain/personalise",{method:"POST",body:d});
export const getNurtureStats=()=>req("/nurture/stats");
export const getEnrolments=(p={})=>req("/nurture/enrolments?"+new URLSearchParams(p));
export const pauseEnrolment=id=>req(`/nurture/enrolments/${id}/pause`,{method:"POST",body:{}});
export const resumeEnrolment=id=>req(`/nurture/enrollments/${id}/resume`,{method:"POST"});
export const getNurtureTracks=()=>req("/nurture/tracks");
export const getBranchingRules=()=>req("/nurture/rules");
