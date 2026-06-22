import Link from "next/link";
import { ArrowRight, ShieldCheck, SplitSquareVertical, Workflow } from "lucide-react";

import { DecisionForm } from "@/components/decision/decision-form";
import { Panel } from "@/components/ui/panel";

const strengths = [
  {
    title: "Scenario intelligence",
    text: "Compare best-case, realistic, and worst-case paths without pretending the future is guaranteed.",
    icon: SplitSquareVertical,
  },
  {
    title: "Evidence-aware reasoning",
    text: "RAG citations make the support visible, while uncertain claims stay labeled as inference.",
    icon: ShieldCheck,
  },
  {
    title: "Feedback policy loop",
    text: "Helpful, saved, and shared decisions become reward signals for better recommendations.",
    icon: Workflow,
  },
];

export default function HomePage() {
  return (
    <main>
      <section className="mx-auto grid max-w-7xl gap-6 px-4 py-8 lg:grid-cols-[0.85fr_1.15fr] lg:py-12">
        <div className="flex flex-col justify-center">
          <p className="text-sm font-semibold uppercase text-signal">AI-powered decision intelligence</p>
          <h1 className="mt-3 max-w-xl text-4xl font-semibold leading-tight sm:text-5xl">
            Simulate choices before they become commitments.
          </h1>
          <p className="mt-4 max-w-xl text-lg leading-8 text-ink/70 dark:text-paper/70">
            FutureYou helps explore plausible futures for career, study, finance, and personal growth decisions with structured trade-offs and source-backed explanations.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link
              href="/decisions/new"
              className="inline-flex h-10 items-center gap-2 rounded-md bg-ink px-4 text-sm font-semibold text-paper transition hover:bg-black dark:bg-paper dark:text-ink"
            >
              Open full form
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              href="/sources"
              className="inline-flex h-10 items-center gap-2 rounded-md border border-line px-4 text-sm font-semibold dark:border-white/10"
            >
              View knowledge base
            </Link>
          </div>
          <div className="mt-8 grid gap-3 sm:grid-cols-3">
            {strengths.map((item) => {
              const Icon = item.icon;
              return (
                <Panel key={item.title} className="p-4">
                  <Icon className="h-5 w-5 text-signal" />
                  <h2 className="mt-3 text-sm font-semibold">{item.title}</h2>
                  <p className="mt-2 text-sm leading-6 text-ink/65 dark:text-paper/65">{item.text}</p>
                </Panel>
              );
            })}
          </div>
        </div>
        <DecisionForm />
      </section>
    </main>
  );
}
