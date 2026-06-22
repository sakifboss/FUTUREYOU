import { ScenarioDashboard } from "@/components/dashboard/scenario-dashboard";

export default function DecisionPage({ params }: { params: { id: string } }) {
  return (
    <main className="mx-auto max-w-7xl px-4 py-8">
      <ScenarioDashboard decisionId={params.id} />
    </main>
  );
}
