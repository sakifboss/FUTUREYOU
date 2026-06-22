import { Library } from "lucide-react";

import { Panel } from "@/components/ui/panel";
import { getSources } from "@/lib/api";
import type { Source } from "@/types/futureyou";

export default async function SourcesPage() {
  let sources: Source[] = [];
  try {
    sources = await getSources();
  } catch {
    sources = [];
  }

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <div className="mb-6 flex items-center gap-3">
        <div className="grid h-10 w-10 place-items-center rounded-md bg-signal text-white">
          <Library className="h-5 w-5" />
        </div>
        <div>
          <p className="text-sm font-semibold uppercase text-signal">Knowledge base</p>
          <h1 className="text-3xl font-semibold">Sources</h1>
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {sources.map((source) => (
          <Panel key={source.id}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <h2 className="font-semibold">{source.title}</h2>
                <p className="mt-1 text-sm text-ink/60 dark:text-paper/60">{source.publisher}</p>
              </div>
              <span className="rounded-md bg-gold/15 px-2 py-1 text-xs text-gold">
                {Math.round(source.reliability_score * 100)}%
              </span>
            </div>
            <p className="mt-3 text-sm leading-6 text-ink/70 dark:text-paper/70">{source.summary}</p>
            <div className="mt-4 flex flex-wrap gap-2">
              {source.tags.map((tag) => (
                <span key={tag} className="rounded-md border border-line px-2 py-1 text-xs dark:border-white/10">
                  {tag}
                </span>
              ))}
            </div>
          </Panel>
        ))}
      </div>
    </main>
  );
}
