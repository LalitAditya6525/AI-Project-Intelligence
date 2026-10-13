
import { useProject } from "../../context/ProjectContext";
import { Activity, CheckCircle2 } from "lucide-react";

function unwrap(data) {
  let result = data;

  // Support common FastAPI response wrappers.
  for (let i = 0; i < 3; i++) {
    if (
      result &&
      typeof result === "object" &&
      result.result &&
      typeof result.result === "object"
    ) {
      result = result.result;
    } else {
      break;
    }
  }

  return result;
}

export default function HealthPage() {
  const { analysis } = useProject();
  const health = unwrap(analysis.health);

  const score =
    health?.overall_score ??
    health?.health_score ??
    health?.score ??
    null;

  const history =
    health?.health_history ??
    health?.score_history ??
    health?.history ??
    [];

  return (
    <div className="space-y-6">
      <section className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6">
        <div className="flex items-center gap-3">
          <Activity className="text-indigo-400" size={24} />
          <h2 className="text-lg font-semibold">
            Project Health
          </h2>
        </div>

        <div className="mt-6">
          <p className="text-sm text-slate-400">
            Overall health score
          </p>

          <p className="mt-2 text-4xl font-bold">
            {typeof score === "number"
              ? `${score}/100`
              : "Not available"}
          </p>

          <p className="mt-2 text-sm text-slate-400">
            {health?.status ??
              health?.health_status ??
              "Run AI Analysis to calculate project health."}
          </p>
        </div>
      </section>

      <section className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6">
        <h3 className="mb-4 font-semibold">
          Health Analysis
        </h3>

        {health ? (
          <div className="space-y-3 text-sm text-slate-300">
            {Object.entries(health).map(([key, value]) => (
              <div
                key={key}
                className="border-b border-slate-800 pb-3"
              >
                <p className="mb-1 capitalize text-slate-500">
                  {key.replaceAll("_", " ")}
                </p>

                <p className="break-words">
                  {typeof value === "object"
                    ? JSON.stringify(value, null, 2)
                    : String(value ?? "—")}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-slate-400">
            No health results yet. Click Run AI Analysis.
          </p>
        )}
      </section>

      {Array.isArray(history) && history.length > 0 && (
        <section className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6">
          <h3 className="mb-3 font-semibold">
            Health Score History
          </h3>

          {history.map((item, index) => (
            <div
              key={index}
              className="flex items-center justify-between border-b border-slate-800 py-3 text-sm"
            >
              <span className="text-slate-400">
                {item.date ?? item.timestamp ?? `Entry ${index + 1}`}
              </span>

              <span className="font-medium">
                {item.score ?? item.health_score ?? "—"}
              </span>
            </div>
          ))}
        </section>
      )}
    </div>
  );
}
