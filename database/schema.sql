-- LeadFlow Database Schema
-- Run this in your Supabase SQL editor

create table if not exists services (id uuid primary key default gen_random_uuid(), created_at timestamptz default now(), offering text not null, best_customers text, wins_losses text, extracted_personas jsonb, extracted_pain_points jsonb, extracted_value_props jsonb, active boolean default true);
create table if not exists campaigns (id uuid primary key default gen_random_uuid(), created_at timestamptz default now(), name text not null, status text default 'draft', icp_criteria jsonb, daily_email_cap integer default 50, min_fit_score integer default 65, notify_email text);
create table if not exists leads (id uuid primary key default gen_random_uuid(), created_at timestamptz default now(), campaign_id uuid references campaigns(id), first_name text, last_name text, email text, linkedin_url text, title text, company text, industry text, location text, source text, fit_score integer, enrichment_data jsonb, ai_first_line text, status text default 'queued', notes text);
create table if not exists outreach_log (id uuid primary key default gen_random_uuid(), created_at timestamptz default now(), lead_id uuid references leads(id), channel text not null, step_number integer, subject text, body text, sent_at timestamptz, opened_at timestamptz, clicked_at timestamptz, replied_at timestamptz, reply_text text, reply_sentiment text);
create table if not exists inboxes (id uuid primary key default gen_random_uuid(), email text unique not null, domain text, status text default 'warming', sent_today integer default 0, daily_cap integer default 40);
create table if not exists signals (id uuid primary key default gen_random_uuid(), name text unique not null, description text, weight integer default 50);
create table if not exists daily_reports (id uuid primary key default gen_random_uuid(), report_date date unique not null default current_date, leads_sourced integer default 0, emails_sent integer default 0, replies integer default 0, hot_replies integer default 0, open_rate numeric, reply_rate numeric);
insert into signals (name, description, weight) values ('hiring_dispatcher','Company hiring dispatchers',95),('recent_funding','Raised Series A/B',82),('fleet_expansion','Hiring drivers',74) on conflict (name) do nothing;
create index if not exists idx_leads_status on leads(status);
