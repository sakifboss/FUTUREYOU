"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowRight, Loader2, Plus, Sparkles } from "lucide-react";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Panel } from "@/components/ui/panel";
import { createDecision, simulateDecision } from "@/lib/api";

const formSchema = z.object({
  title: z.string().optional(),
  current_age: z.coerce.number().min(13).max(90),
  country_location: z.string().min(2),
  current_situation: z.string().min(10),
  goal: z.string().min(5),
  option_lines: z.string().min(8),
  risk_tolerance: z.enum(["low", "medium", "high"]),
  time_horizon: z.string().min(2),
  budget_constraints: z.string().optional(),
  skills: z.string().optional(),
  personality_preferences: z.string().optional(),
});

type FormValues = z.infer<typeof formSchema>;

const defaults: FormValues = {
  title: "AI career path decision",
  current_age: 22,
  country_location: "Dhaka, Bangladesh",
  current_situation:
    "I am learning software development and want a practical path that can create career momentum.",
  goal: "Choose between focusing on AI application development or full-stack web development.",
  option_lines:
    "AI application development - Build RAG apps, automations, and model-integrated products\nFull-stack web development - Build production web apps and backend systems",
  risk_tolerance: "medium",
  time_horizon: "6 to 12 months",
  budget_constraints: "Limited budget, CPU-only laptop, needs lightweight learning plan",
  skills: "JavaScript, Python, React, basic backend",
  personality_preferences: "Prefers practical projects and visible progress",
};

export function DecisionForm() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [stage, setStage] = useState<string | null>(null);
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: defaults,
  });

  async function onSubmit(values: FormValues) {
    setError(null);
    setStage("Creating decision model");
    const options = values.option_lines
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => {
        const [label, description] = line.split(" - ");
        return { label: label.trim(), description: description?.trim() };
      });

    if (options.length < 2) {
      setError("Add at least two options, one per line.");
      setStage(null);
      return;
    }

    try {
      const decision = await createDecision({
        title: values.title,
        current_age: values.current_age,
        country_location: values.country_location,
        current_situation: values.current_situation,
        goal: values.goal,
        options,
        risk_tolerance: values.risk_tolerance,
        time_horizon: values.time_horizon,
        budget_constraints: values.budget_constraints,
        skills: values.skills?.split(",").map((skill) => skill.trim()).filter(Boolean) || [],
        personality_preferences: values.personality_preferences,
      });
      setStage("Retrieving sources and simulating scenarios");
      await simulateDecision(decision.id);
      router.push(`/decisions/${decision.id}`);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Could not create the simulation.");
      setStage(null);
    }
  }

  const inputClass =
    "mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-sm outline-none transition focus:border-signal focus:ring-2 focus:ring-signal/20 dark:border-white/10 dark:bg-white/[0.06]";
  const labelClass = "text-sm font-medium text-ink/75 dark:text-paper/75";

  return (
    <Panel className="p-4 sm:p-6">
      <div className="mb-5 flex items-center justify-between gap-3">
        <div>
          <p className="text-sm font-semibold uppercase text-signal">Decision simulator</p>
          <h1 className="mt-1 text-2xl font-semibold sm:text-3xl">Build a FutureYou scenario</h1>
        </div>
        <div className="hidden rounded-md border border-line px-3 py-2 text-sm dark:border-white/10 sm:block">
          RAG + policy feedback
        </div>
      </div>

      <form onSubmit={form.handleSubmit(onSubmit)} className="grid gap-4">
        <div className="grid gap-4 md:grid-cols-2">
          <label className={labelClass}>
            Decision title
            <input className={inputClass} {...form.register("title")} />
          </label>
          <label className={labelClass}>
            Current age
            <input type="number" className={inputClass} {...form.register("current_age")} />
          </label>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <label className={labelClass}>
            Country / location
            <input className={inputClass} {...form.register("country_location")} />
          </label>
          <label className={labelClass}>
            Time horizon
            <input className={inputClass} {...form.register("time_horizon")} />
          </label>
        </div>

        <label className={labelClass}>
          Current situation
          <textarea rows={3} className={inputClass} {...form.register("current_situation")} />
        </label>

        <label className={labelClass}>
          Goal
          <textarea rows={2} className={inputClass} {...form.register("goal")} />
        </label>

        <label className={labelClass}>
          Decision options
          <textarea rows={4} className={inputClass} {...form.register("option_lines")} />
        </label>

        <div className="grid gap-4 md:grid-cols-3">
          <label className={labelClass}>
            Risk tolerance
            <select className={inputClass} {...form.register("risk_tolerance")}>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </label>
          <label className={labelClass}>
            Budget / constraints
            <input className={inputClass} {...form.register("budget_constraints")} />
          </label>
          <label className={labelClass}>
            Skills
            <input className={inputClass} {...form.register("skills")} />
          </label>
        </div>

        <label className={labelClass}>
          Personality preferences
          <input className={inputClass} {...form.register("personality_preferences")} />
        </label>

        {Object.keys(form.formState.errors).length > 0 && (
          <p className="rounded-md border border-coral/30 bg-coral/10 px-3 py-2 text-sm text-coral">
            Please check the highlighted fields. The simulator needs enough context to work.
          </p>
        )}
        {error && (
          <p className="rounded-md border border-coral/30 bg-coral/10 px-3 py-2 text-sm text-coral">
            {error}
          </p>
        )}
        {stage && (
          <p className="inline-flex items-center gap-2 text-sm text-signal">
            <Loader2 className="h-4 w-4 animate-spin" />
            {stage}
          </p>
        )}

        <div className="flex flex-col gap-3 sm:flex-row">
          <Button type="submit" disabled={form.formState.isSubmitting}>
            {form.formState.isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
            Generate simulation
            <ArrowRight className="h-4 w-4" />
          </Button>
          <Button
            type="button"
            variant="secondary"
            onClick={() => {
              const current = form.getValues("option_lines");
              form.setValue("option_lines", `${current}\nRemote freelancing - Test market demand with small client projects`);
            }}
          >
            <Plus className="h-4 w-4" />
            Add sample option
          </Button>
        </div>
      </form>
    </Panel>
  );
}
