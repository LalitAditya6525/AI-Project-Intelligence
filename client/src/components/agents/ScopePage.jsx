import { useProject } from "../../context/ProjectContext";
import { Target } from "lucide-react";

function unwrap(data) {
  let result = data;

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

function ResultList({ title, items }) {
  if (!Array.isArray(items) || items.length === 0) {
    return null;
  }

  return (
    <section className="rounded-xl border border-slate-800 bg-slate-900/50 p-5">
      <h3 className="mb-3 font-semibold">{title}</h3>

      <ul className="list-inside list-disc space-y-2 text-sm text-slate-300">
        {items.map((item, index) => (
          <li key={index}>
            {typeof item === "string"
              ? item
              : item.title ??
                item.name ??
                item.description ??
                JSON.stringify(item)}
          </li>
        ))}
      </ul>
    </section>
  );
}

export default function ScopePage() {
  const { analysis } = useProject();
  const scope = unwrap(analysis.scope);

  if (!scope) {
    return (
      <div className="rounded-xl border border-slate-800 p-6 text-slate-400">
        No scope results yet. Click Run AI Analysis.
      </div>
    );
  }

  return (
    <div className="space-y-5">
      <section className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">
        <div className="mb-4 flex items-center gap-3">
          <Target className="text-indigo-400" size={23} />
          <h2 className="text-lg font-semibold">
            Project Scope
          </h2>
        </div>

        <p className="whitespace-pre-wrap text-sm leading-7 text-slate-300">
          {scope.project_goal ??
            scope.scope_summary ??
            scope.summary ??
            scope.description ??
            "The response contains no recognized project goal field."}
        </p>
      </section>

      <ResultList
        title="Major Deliverables"
        items={scope.major_deliverables ?? scope.deliverables}
      />

      <ResultList
        title="Milestones"
        items={scope.milestones}
      />

      <ResultList
        title="Deadlines"
        items={scope.deadlines ?? scope.important_project_dates}
      />

      <ResultList
        title="Team Responsibilities"
        items={scope.team_responsibilities}
      />

      <details className="rounded-xl border border-slate-800 p-4">
        <summary className="cursor-pointer text-sm text-slate-400">
          Inspect raw backend response
        </summary>

        <pre className="mt-4 overflow-auto whitespace-pre-wrap break-words text-xs text-slate-300">
          {JSON.stringify(scope, null, 2)}
        </pre>
      </details>
    </div>
  );
}
