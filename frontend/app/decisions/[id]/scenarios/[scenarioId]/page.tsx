import Link from "next/link";
import { ArrowLeft } from "lucide-react";

import { API_BASE_URL } from "@/lib/api";
import { percent } from "@/lib/utils";
import type { Scenario } from "@/types/futureyou";

type DecisionDetail = {
  title: string;
  scenarios: Scenario[];
  options: Array<{ id: string; label: string }>;
};

async function getDecision(id: string): Promise<DecisionDetail | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/decisions/${id}`, { cache: "no-store" });
    if (!response.ok) return null;
    return response.json();
  } catch {
    return null;
  }
}

export default async function ScenarioDetailPage({
  params,
}: {
  params: { id: string; scenarioId: string };
}) {
  const decision = await getDecision(params.id);
  const scenario = decision?.scenarios.find((item) => item.id === params.scenarioId);
  const option = decision?.options.find((item) => item.id === scenario?.option_id);

  if (!decision || !scenario) {
    return (
      <main className="mx-auto max-w-4xl px-4 py-8">
        <Link href={`/decisions/${params.id}`} className="inline-flex items-center gap-2 text-sm text-signal">
          <ArrowLeft className="h-4 w-4" />
          Back to dashboard
        </Link>
        <h1 className="mt-6 text-2xl font-semibold">Scenario not found</h1>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-4xl px-4 py-8">
      <Link href={`/decisions/${params.id}`} className="inline-flex items-center gap-2 text-sm text-signal">
        <ArrowLeft className="h-4 w-4" />
        Back to dashboard
      </Link>
      <article className="mt-6 rounded-lg border border-line bg-white p-6 shadow-sm dark:border-white/10 dark:bg-white/[0.06]">
        <p className="text-sm font-semibold uppercase text-signal">{option?.label}</p>
        <h1 className="mt-2 text-3xl font-semibold">{scenario.title}</h1>
        <p className="mt-4 leading-8 text-ink/75 dark:text-paper/75">{scenario.narrative}</p>

        <div className="mt-6 grid gap-3 sm:grid-cols-4">
          <Stat label="Probability" value={percent(scenario.probability)} />
          <Stat label="Risk" value={percent(scenario.risk_level)} />
          <Stat label="Opportunity" value={percent(scenario.opportunity_level)} />
          <Stat label="Effort" value={percent(scenario.effort_level)} />
        </div>

        <div className="mt-8 grid gap-6 md:grid-cols-2">
          <Section title="Major risks" items={scenario.major_risks} />
          <Section title="Major opportunities" items={scenario.major_opportunities} />
        </div>

        <div className="mt-8">
          <h2 className="text-lg font-semibold">Action path</h2>
          <ol className="mt-4 grid gap-3">
            {scenario.action_path.map((item, index) => (
              <li key={item} className="flex gap-3">
                <span className="grid h-7 w-7 shrink-0 place-items-center rounded-md bg-signal text-sm text-white">
                  {index + 1}
                </span>
                <span>{item}</span>
              </li>
            ))}
          </ol>
        </div>
      </article>
    </main>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-line p-3 dark:border-white/10">
      <p className="text-xl font-semibold">{value}</p>
      <p className="mt-1 text-xs uppercase text-ink/55 dark:text-paper/55">{label}</p>
    </div>
  );
}

function Section({ title, items }: { title: string; items: string[] }) {
  return (
    <section>
      <h2 className="text-lg font-semibold">{title}</h2>
      <ul className="mt-3 grid gap-2 text-sm leading-6 text-ink/75 dark:text-paper/75">
        {items.map((item) => (
          <li key={item} className="rounded-md border border-line p-3 dark:border-white/10">
            {item}
          </li>
        ))}
      </ul>
    </section>
  );
}
