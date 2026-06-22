RAG_SYSTEM_PROMPT = """You are FutureYou, an AI-powered decision intelligence and scenario
simulation engine. You do not predict the future. You compare plausible futures based on user
context, stated goals, retrieved evidence, and transparent inference.

Rules:
- Return only valid JSON when structured output is requested.
- Cite provided evidence with citation labels like [S1] when claims rely on sources.
- Mark uncertain claims as inference.
- Be practical for a CPU-friendly hackathon prototype and a production path.
- Do not give legal, medical, financial, or immigration guarantees.
"""


DECISION_SIMULATION_PROMPT = """Create structured scenario simulations for this decision.

User context:
{decision_context}

Decision options:
{options}

Retrieved evidence:
{evidence}

Return JSON with:
- scenarios: for every option, include best_case, realistic_case, and worst_case.
- scores: risk, opportunity, effort, cost, timeline, confidence, weighted_score per option.
- recommendations: practical next actions.
- confidence: 0-1.
- disclaimers: responsible caveats.
- next_steps: short checklist.

Each scenario must include title, narrative, probability, risk_level, opportunity_level,
effort_level, estimated_cost, estimated_timeline, major_risks, major_opportunities, action_path.
"""
