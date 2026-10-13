import { useState } from "react";
import {
  Play,
  LoaderCircle,
  AlertCircle,
} from "lucide-react";

import Header from "../components/Header";
import Sidebar from "../components/Sidebar";

import HealthPage from "../components/agents/HealthPage";
import ScopePage from "../components/agents/ScopePage";
import DeliverablesPage from "../components/agents/DeliverablesPage";
import RiskPage from "../components/agents/RiskPage";
import BlockerPage from "../components/agents/BlockerPage";
import DocumentationPage from "../components/agents/DocumentationPage";

import { useProject } from "../context/ProjectContext";

import {
  runScopeAgent,
  runRiskAgent,
  runBlockerAgent,
  runDocumentationAgent,
  runHealthAgent,
} from "../services/api";

const agentTasks = [
  ["scope", runScopeAgent],
  ["risk", runRiskAgent],
  ["blocker", runBlockerAgent],
  ["documentation", runDocumentationAgent],
  ["health", runHealthAgent],
];

const pages = {
  health: HealthPage,
  scope: ScopePage,
  deliverables: DeliverablesPage,
  risk: RiskPage,
  blocker: BlockerPage,
  documentation: DocumentationPage,
};

const titles = {
  health: "Health",
  scope: "Scope",
  deliverables: "Deliverables",
  risk: "Risks",
  blocker: "Blockers",
  documentation: "Documentation",
};

export default function Dashboard({
  project,
  onNewProject,
}) {
  const {
    activePage,
    setActivePage,
    analysis,
    updateAnalysis,
    loading,
    setLoading,
  } = useProject();

  const [errors, setErrors] = useState([]);
  const [successMessage, setSuccessMessage] = useState("");

  const ActivePage = pages[activePage] || HealthPage;

  const runAnalysis = async () => {
    setLoading(true);
    setErrors([]);
    setSuccessMessage("");

    const failures = [];
    let completed = 0;

    try {
      const results = await Promise.allSettled(
        agentTasks.map(async ([key, runAgent]) => {
          const response = await runAgent();

          // Preserve the raw response. Each page can unwrap
          // response.result if the backend uses that structure.
          updateAnalysis(key, response);

          completed += 1;
          return { key, response };
        })
      );

      results.forEach((result, index) => {
        if (result.status === "rejected") {
          failures.push({
            agent: agentTasks[index][0],
            message:
              result.reason?.response?.data?.detail ||
              result.reason?.message ||
              "Request failed",
          });
        }
      });

      setErrors(failures);

      if (completed > 0) {
        setSuccessMessage(
          `${completed} of ${agentTasks.length} agents completed successfully.`
        );
      }

      // Deliverables may be returned by scope or documentation.
      // Reuse existing results rather than inventing an endpoint.
      const scopeResult =
        results[0]?.status === "fulfilled"
          ? results[0].value.response
          : analysis.scope;

      const documentationResult =
        results[3]?.status === "fulfilled"
          ? results[3].value.response
          : analysis.documentation;

      if (scopeResult || documentationResult) {
        updateAnalysis("deliverables", {
          items: [
            ...(scopeResult?.major_deliverables ||
              scopeResult?.result?.major_deliverables ||
              []),
            ...(documentationResult?.deliverables ||
              documentationResult?.result?.deliverables ||
              []),
          ],
        });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#070d19] text-white">
      <Header
        projectName={project?.projectName}
        onNewProject={onNewProject}
      />

      <div className="grid min-h-[calc(100vh-64px)] grid-cols-1 md:grid-cols-[240px_minmax(0,1fr)]">
        <Sidebar
          activePage={activePage}
          onNavigate={setActivePage}
          onNewProject={onNewProject}
        />

        <main className="min-w-0 p-5 sm:p-8">
          <div className="mb-6 flex flex-col justify-between gap-4 border-b border-slate-800 pb-5 sm:flex-row sm:items-center">
            <div>
              <p className="text-xs uppercase tracking-widest text-slate-500">
                {project?.projectName || "Project Workspace"}
              </p>

              <h1 className="mt-2 text-2xl font-semibold">
                Current Agent Results
              </h1>

              <p className="mt-2 text-sm text-slate-400">
                Viewing: {titles[activePage] || "Health"}
              </p>
            </div>

            <button
              onClick={runAnalysis}
              disabled={loading}
              className="flex shrink-0 items-center justify-center gap-2 rounded-xl bg-indigo-500 px-5 py-3 text-sm font-semibold hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? (
                <LoaderCircle
                  size={18}
                  className="animate-spin"
                />
              ) : (
                <Play size={18} />
              )}

              {loading ? "Analyzing..." : "Run AI Analysis"}
            </button>
          </div>

          {successMessage && (
            <div className="mb-4 rounded-lg border border-emerald-800 bg-emerald-500/10 p-3 text-sm text-emerald-300">
              {successMessage}
            </div>
          )}

          {errors.length > 0 && (
            <div className="mb-5 rounded-xl border border-red-900 bg-red-500/10 p-4">
              <div className="mb-2 flex items-center gap-2 font-medium text-red-300">
                <AlertCircle size={18} />
                Some agents failed
              </div>

              {errors.map((error) => (
                <p
                  key={error.agent}
                  className="mt-1 text-sm text-red-200"
                >
                  {error.agent}: {error.message}
                </p>
              ))}
            </div>
          )}

          <ActivePage />
        </main>
      </div>
    </div>
  );
}
