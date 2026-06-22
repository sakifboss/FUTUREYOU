export type RiskTolerance = "low" | "medium" | "high";

export type DecisionCreate = {
  title?: string;
  current_age: number;
  country_location: string;
  current_situation: string;
  goal: string;
  options: Array<{ label: string; description?: string }>;
  risk_tolerance: RiskTolerance;
  time_horizon: string;
  budget_constraints?: string;
  skills: string[];
  personality_preferences?: string;
};

export type Scenario = {
  id: string;
  decision_id: string;
  option_id: string;
  scenario_type: string;
  title: string;
  narrative: string;
  probability: number;
  risk_level: number;
  opportunity_level: number;
  effort_level: number;
  estimated_cost: string;
  estimated_timeline: string;
  major_risks: string[];
  major_opportunities: string[];
  action_path: string[];
};

export type Score = {
  option_id: string;
  option_label: string;
  risk: number;
  opportunity: number;
  effort: number;
  cost: number;
  timeline: number;
  confidence: number;
  weighted_score: number;
};

export type Citation = {
  id: string;
  label: string;
  title: string;
  url: string;
  publisher: string;
  source_type: string;
  snippet: string;
  relevance_score: number;
};

export type SimulationResponse = {
  decision_summary: {
    id: string;
    title: string;
    goal: string;
    current_age: number;
    country_location: string;
    risk_tolerance: string;
    time_horizon: string;
    status: string;
    share_token: string;
  };
  options: Array<{
    id: string;
    label: string;
    description?: string;
    policy_score: number;
  }>;
  scenarios: Scenario[];
  scores: Score[];
  recommendations: Array<{
    option_id?: string;
    title: string;
    rationale: string;
    action_items: string[];
  }>;
  citations: Citation[];
  confidence: number;
  disclaimers: string[];
  next_steps: string[];
};

export type DecisionListItem = {
  id: string;
  title: string;
  goal: string;
  country_location: string;
  risk_tolerance: string;
  status: string;
  created_at: string;
  updated_at: string;
  option_count: number;
  scenario_count: number;
};

export type Source = {
  id: string;
  title: string;
  url: string;
  publisher: string;
  source_type: string;
  country?: string;
  summary: string;
  tags: string[];
  reliability_score: number;
  created_at: string;
};
