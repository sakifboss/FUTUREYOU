"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { Download, Loader2, RefreshCw, Share2 } from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Button } from "@/components/ui/button";
import { Panel } from "@/components/ui/panel";
import { API_BASE_URL, regenerateDecision, simulateDecision } from "@/lib/api";
import { percent } from "@/lib/utils";
import type { SimulationResponse } from "@/types/futureyou";

export function ScenarioDashboard({ decisionId }: { decisionId: string }) {
  const [data, setData] = useState<SimulationResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      setData(await simulateDecision(decisionId));
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to load simulation.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [decisionId]);

  const chartData = useMemo(
    () =>
      data?.scores.map((score) => ({
        option: score.option_label,
        risk: Math.round(score.risk * 100),
        opportunity: Math.round(score.opportunity * 100),
        effort: Math.round(score.effort * 100),
        score: Math.round(score.weighted_score * 100),
      })) || [],
    [data],
  );

  if (loading) {
    return (
      <Panel className="flex min-h-[360px] items-center justify-center">
        <div className="text-center">
          <Loader2 className="mx-auto h-7 w-7 animate-spin text-signal" />
          <p className="mt-3 font-medium">Building scenario dashboard</p>
          <p className="mt-1 text-sm text-ink/60 dark:text-paper/60">Retrieving sources and scoring trade-offs.</p>
        </div>
      </Panel>
    );
  }

  if (error || !data) {
    return (
      <Panel>
        <p className="font-semibold text-coral">Dashboard could not load</p>
        <p className="mt-2 text-sm text-ink/70 dark:text-paper/70">{error}</p>
        <Button className="mt-4" onClick={load}>Try again</Button>
      </Panel>
    );
  }

  return (
    <div className="grid gap-5">
      <Panel>
        <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-start">
          <div>
            <p className="text-sm font-semibold uppercase text-signal">Decision summary</p>
            <h1 className="mt-1 text-2xl font-semibold sm:text-3xl">{data.decision_summary.title}</h1>
            <p className="mt-3 max-w-3xl text-ink/70 dark:text-paper/70">{data.decision_summary.goal}</p>
            <div className="mt-4 flex flex-wrap gap-2 text-sm">
              <span className="rounded-md border border-line px-3 py-1 dark:border-white/10">
                {data.decision_summary.country_location}
              </span>
              <span className="rounded-md border border-line px-3 py-1 dark:border-white/10">
                Risk: {data.decision_summary.risk_tolerance}
              </span>
              <span className="rounded-md border border-line px-3 py-1 dark:border-white/10">
                Horizon: {data.decision_summary.time_horizon}
              </span>
              <span className="rounded-md border border-line px-3 py-1 dark:border-white/10">
                Confidence: {percent(data.confidence)}
              </span>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button
              variant="secondary"
              onClick={async () => {
                setLoading(true);
                setData(await regenerateDecision(decisionId));
                setLoading(false);
              }}
            >
              <RefreshCw className="h-4 w-4" />
              Regenerate
            </Button>
            <a href={`${API_BASE_URL}/api/decisions/${decisionId}/export`}>
              <Button variant="secondary">
                <Download className="h-4 w-4" />
                Export PDF
              </Button>
            </a>
            <Button
              variant="ghost"
              onClick={() => navigator.clipboard.writeText(window.location.href)}
            >
              <Share2 className="h-4 w-4" />
              Share
            </Button>
          </div>
        </div>
      </Panel>

      <div className="grid gap-5 lg:grid-cols-[1.2fr_0.8fr]">
        <Panel>
          <h2 className="text-lg font-semibold">Risk vs reward</h2>
          <div className="mt-4 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#d9d2c7" />
                <XAxis dataKey="option" tickLine={false} />
                <YAxis tickFormatter={(value) => `${value}%`} />
                <Tooltip />
                <Legend />
                <Bar dataKey="opportunity" fill="#0f766e" radius={[4, 4, 0, 0]} />
                <Bar dataKey="risk" fill="#be4b45" radius={[4, 4, 0, 0]} />
                <Bar dataKey="score" fill="#c58b22" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel>
          <h2 className="text-lg font-semibold">Recommended next steps</h2>
          <ol className="mt-4 grid gap-3">
            {data.next_steps.map((step, index) => (
              <li key={step} className="flex gap-3 text-sm">
                <span className="grid h-6 w-6 shrink-0 place-items-center rounded-md bg-signal text-white">
                  {index + 1}
                </span>
                <span>{step}</span>
              </li>
            ))}
          </ol>
        </Panel>
      </div>

      <section className="grid gap-4 lg:grid-cols-3">
        {data.scenarios.map((scenario) => {
          const option = data.options.find((item) => item.id === scenario.option_id);
          return (
            <Link key={scenario.id} href={`/decisions/${decisionId}/scenarios/${scenario.id}`}>
              <Panel className="h-full transition hover:-translate-y-0.5 hover:shadow-soft">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-xs font-semibold uppercase text-signal">{option?.label}</p>
                    <h3 className="mt-1 font-semibold">{scenario.title}</h3>
                  </div>
                  <span className="rounded-md bg-ink px-2 py-1 text-xs text-paper dark:bg-paper dark:text-ink">
                    {percent(scenario.probability)}
                  </span>
                </div>
                <p className="mt-3 text-sm leading-6 text-ink/70 dark:text-paper/70">{scenario.narrative}</p>
                <div className="mt-4 grid grid-cols-3 gap-2 text-center text-xs">
                  <Metric label="Risk" value={scenario.risk_level} tone="risk" />
                  <Metric label="Reward" value={scenario.opportunity_level} tone="reward" />
                  <Metric label="Effort" value={scenario.effort_level} tone="effort" />
                </div>
              </Panel>
            </Link>
          );
        })}
      </section>

      <div className="grid gap-5 lg:grid-cols-2">
        <Panel>
          <h2 className="text-lg font-semibold">Recommendations</h2>
          <div className="mt-4 grid gap-4">
            {data.recommendations.map((recommendation) => (
              <div key={recommendation.title} className="rounded-md border border-line p-4 dark:border-white/10">
                <h3 className="font-semibold">{recommendation.title}</h3>
                <p className="mt-2 text-sm text-ink/70 dark:text-paper/70">{recommendation.rationale}</p>
                <ul className="mt-3 grid gap-2 text-sm">
                  {recommendation.action_items.map((item) => (
                    <li key={item} className="flex gap-2">
                      <span className="mt-2 h-1.5 w-1.5 rounded-full bg-signal" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </Panel>

        <Panel>
          <h2 className="text-lg font-semibold">Sources and citations</h2>
          <div className="mt-4 grid gap-3">
            {data.citations.map((citation) => (
              <a
                key={`${citation.label}-${citation.id}`}
                href={citation.url}
                target="_blank"
                rel="noreferrer"
                className="rounded-md border border-line p-3 transition hover:border-signal dark:border-white/10"
              >
                <p className="text-sm font-semibold">
                  [{citation.label}] {citation.title}
                </p>
                <p className="mt-1 text-xs text-ink/60 dark:text-paper/60">{citation.publisher}</p>
                <p className="mt-2 text-sm text-ink/70 dark:text-paper/70">{citation.snippet}</p>
              </a>
            ))}
          </div>
        </Panel>
      </div>
    </div>
  );
}

function Metric({ label, value, tone }: { label: string; value: number; tone: "risk" | "reward" | "effort" }) {
  const color = tone === "risk" ? "bg-coral" : tone === "reward" ? "bg-signal" : "bg-gold";
  return (
    <div className="rounded-md border border-line p-2 dark:border-white/10">
      <p className="font-semibold">{percent(value)}</p>
      <div className="mt-2 h-1.5 rounded-full bg-black/10 dark:bg-white/10">
        <div className={`h-1.5 rounded-full ${color}`} style={{ width: percent(value) }} />
      </div>
      <p className="mt-2 text-ink/60 dark:text-paper/60">{label}</p>
    </div>
  );
}
