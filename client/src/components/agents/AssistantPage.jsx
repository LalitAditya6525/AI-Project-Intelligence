import {
  Activity,
  BarChart3,
} from "lucide-react";

import Sidebar from "../components/Sidebar";
import { useProject } from "../context/ProjectContext";

const HealthBar = ({ label, score }) => {
  const value =
    typeof score === "number" ? score : 0;

  return (
    <div>

      <div className="mb-2 flex items-center justify-between">

        <span className="text-sm text-slate-400">
          {label}
        </span>

        <span className="text-sm font-semibold text-white">
          {score ?? "--"}
        </span>

      </div>

      <div className="h-2 overflow-hidden rounded-full bg-slate-800">

        <div
          className="h-full rounded-full bg-indigo-500 transition-all"
          style={{
            width: `${Math.min(
              Math.max(value, 0),
              100
            )}%`,
          }}
        />

      </div>

    </div>
  );
};

const HealthPage = () => {
  const { analysis } = useProject();

  const health = analysis.health || {};

  return (
    <div className="flex min-h-screen bg-[#0f1117]">

      <Sidebar />

      <main className="flex-1 p-8">

        <div className="mx-auto max-w-5xl">

          <div className="mb-10 flex items-center gap-4">

            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-500/10">
              <BarChart3
                size={24}
                className="text-indigo-400"
              />
            </div>

            <div>
              <h1 className="text-3xl font-bold text-white">
                Project Health
              </h1>

              <p className="mt-1 text-slate-500">
                Overall project health and dimension-wise
                assessment.
              </p>
            </div>

          </div>

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">

            <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-8 text-center">

              <p className="text-sm text-slate-500">
                Overall Health
              </p>

              <p className="mt-4 text-6xl font-bold text-white">
                {health.overall_score ?? "--"}
              </p>

              <p className="mt-3 text-sm text-slate-500">
                out of 100
              </p>

            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-8 lg:col-span-2">

              <div className="mb-7 flex items-center gap-3">

                <Activity
                  size={20}
                  className="text-indigo-400"
                />

                <h2 className="font-semibold text-white">
                  Health Dimensions
                </h2>

              </div>

              <div className="space-y-6">

                <HealthBar
                  label="Scope Clarity"
                  score={
                    health.scope_clarity
                  }
                />

                <HealthBar
                  label="Timeline Health"
                  score={
                    health.timeline_health
                  }
                />

                <HealthBar
                  label="Risk Health"
                  score={
                    health.risk_health
                  }
                />

                <HealthBar
                  label="Blocker Health"
                  score={
                    health.blocker_health
                  }
                />

              </div>

            </div>

          </div>

          {health.summary && (
            <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/70 p-6">

              <h2 className="font-semibold text-white">
                Health Summary
              </h2>

              <p className="mt-3 text-sm leading-7 text-slate-400">
                {health.summary}
              </p>

            </div>
          )}

          {health.dimension_analysis && (
            <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2">

              {Object.entries(
                health.dimension_analysis
              ).map(([key, value]) => (
                <div
                  key={key}
                  className="rounded-xl border border-slate-800 bg-slate-900/70 p-5"
                >

                  <h3 className="text-sm font-semibold capitalize text-white">
                    {key.replaceAll("_", " ")}
                  </h3>

                  <p className="mt-2 text-sm leading-6 text-slate-500">
                    {value}
                  </p>

                </div>
              ))}

            </div>
          )}

          {health.evidence?.length > 0 && (
            <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/70 p-6">

              <h2 className="font-semibold text-white">
                Evidence
              </h2>

              <ul className="mt-4 space-y-3">

                {health.evidence.map(
                  (item, index) => (
                    <li
                      key={index}
                      className="text-sm text-slate-400"
                    >
                      • {item}
                    </li>
                  )
                )}

              </ul>

            </div>
          )}

        </div>

      </main>

    </div>
  );
};

export default HealthPage;