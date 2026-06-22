import { Settings } from "lucide-react";

import { Panel } from "@/components/ui/panel";
import { API_BASE_URL } from "@/lib/api";

export default function SettingsPage() {
  return (
    <main className="mx-auto max-w-4xl px-4 py-8">
      <div className="mb-6 flex items-center gap-3">
        <div className="grid h-10 w-10 place-items-center rounded-md bg-ink text-paper dark:bg-paper dark:text-ink">
          <Settings className="h-5 w-5" />
        </div>
        <div>
          <p className="text-sm font-semibold uppercase text-signal">Runtime</p>
          <h1 className="text-3xl font-semibold">Settings</h1>
        </div>
      </div>
      <Panel>
        <dl className="grid gap-4">
          <div className="rounded-md border border-line p-4 dark:border-white/10">
            <dt className="text-sm font-semibold text-ink/60 dark:text-paper/60">Backend API</dt>
            <dd className="mt-1 font-mono text-sm">{API_BASE_URL}</dd>
          </div>
          <div className="rounded-md border border-line p-4 dark:border-white/10">
            <dt className="text-sm font-semibold text-ink/60 dark:text-paper/60">LLM mode</dt>
            <dd className="mt-1 text-sm">Backend configured by environment: mock, Ollama, or OpenAI-compatible.</dd>
          </div>
          <div className="rounded-md border border-line p-4 dark:border-white/10">
            <dt className="text-sm font-semibold text-ink/60 dark:text-paper/60">Positioning</dt>
            <dd className="mt-1 text-sm">Scenario simulation and decision intelligence, not future prediction.</dd>
          </div>
        </dl>
      </Panel>
    </main>
  );
}
