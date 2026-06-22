import Link from "next/link";
import { Clock3 } from "lucide-react";

import { Panel } from "@/components/ui/panel";
import { getDecisions } from "@/lib/api";
import type { DecisionListItem } from "@/types/futureyou";

export default async function HistoryPage() {
  let decisions: DecisionListItem[] = [];
  try {
    decisions = await getDecisions();
  } catch {
    decisions = [];
  }

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <div className="mb-6">
        <p className="text-sm font-semibold uppercase text-signal">Saved decisions</p>
        <h1 className="mt-1 text-3xl font-semibold">History</h1>
      </div>
      <div className="grid gap-4">
        {decisions.length === 0 && (
          <Panel>
            <p className="font-medium">No saved decisions yet.</p>
            <p className="mt-2 text-sm text-ink/65 dark:text-paper/65">Create a simulation to see it here.</p>
          </Panel>
        )}
        {decisions.map((decision) => (
          <Link key={decision.id} href={`/decisions/${decision.id}`}>
            <Panel className="transition hover:-translate-y-0.5 hover:shadow-soft">
              <div className="flex flex-col justify-between gap-3 sm:flex-row">
                <div>
                  <h2 className="text-lg font-semibold">{decision.title}</h2>
                  <p className="mt-2 text-sm text-ink/70 dark:text-paper/70">{decision.goal}</p>
                </div>
                <div className="flex shrink-0 items-center gap-2 text-sm text-ink/60 dark:text-paper/60">
                  <Clock3 className="h-4 w-4" />
                  {new Date(decision.updated_at).toLocaleDateString()}
                </div>
              </div>
              <div className="mt-4 flex flex-wrap gap-2 text-xs">
                <span className="rounded-md border border-line px-2 py-1 dark:border-white/10">{decision.country_location}</span>
                <span className="rounded-md border border-line px-2 py-1 dark:border-white/10">{decision.option_count} options</span>
                <span className="rounded-md border border-line px-2 py-1 dark:border-white/10">{decision.scenario_count} scenarios</span>
              </div>
            </Panel>
          </Link>
        ))}
      </div>
    </main>
  );
}
