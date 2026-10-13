import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Calendar,
  FolderPlus,
  Sparkles,
} from "lucide-react";

import FileUpload from "./FileUpload";
import LoadingAnalysis from "./LoadingAnalysis";

import {
  uploadDocuments,
  runScopeAgent,
  runRiskAgent,
  runBlockerAgent,
  runDocumentationAgent,
  runHealthAgent,
} from "../services/api";

import { useProject } from "../context/ProjectContext";

const ProjectForm = () => {
  const navigate = useNavigate();

  const {
    setProject,
    setDocuments,
    updateAnalysis,
    setLoading,
  } = useProject();

  const [form, setForm] = useState({
    name: "",
    description: "",
    startDate: "",
    endDate: "",
    status: "Not Started",
  });

  const [files, setFiles] = useState([]);

  const [analyzing, setAnalyzing] = useState(false);

  const [currentStep, setCurrentStep] = useState(
    "Waiting to start"
  );

  const updateField = (field, value) => {
    setForm((previous) => ({
      ...previous,
      [field]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!form.name.trim()) {
      alert("Please enter a project name.");
      return;
    }

    if (!form.description.trim()) {
      alert("Please enter a project description.");
      return;
    }

    if (!form.startDate || !form.endDate) {
      alert("Please select project dates.");
      return;
    }

    if (files.length === 0) {
      alert("Please upload at least one project document.");
      return;
    }

    setAnalyzing(true);
    setLoading(true);

    try {
      setCurrentStep("Uploading documents...");

      const uploadResponse =
        await uploadDocuments(files);

      if (uploadResponse.status !== 200) {
        throw new Error("Document upload failed.");
      }

      setDocuments(files);

      const projectId = `project-${Date.now()}`;

      setProject({
        ...form,
        id: projectId,
      });

      navigate(`/project/${projectId}`);

      setCurrentStep("Analyzing project scope...");

      const scopeResponse =
        await runScopeAgent();

      updateAnalysis(
        "scope",
        scopeResponse.data.result
      );

      setCurrentStep("Detecting project risks...");

      const riskResponse =
        await runRiskAgent();

      updateAnalysis(
        "risk",
        riskResponse.data.result
      );

      setCurrentStep("Detecting blockers and action items...");

      const blockerResponse =
        await runBlockerAgent();

      updateAnalysis(
        "blocker",
        blockerResponse.data.result
      );

      setCurrentStep(
        "Generating project documentation..."
      );

      const documentationResponse =
        await runDocumentationAgent();

      updateAnalysis(
        "documentation",
        documentationResponse.data.result
      );

      setCurrentStep(
        "Calculating project health..."
      );

      const healthResponse =
        await runHealthAgent();

      updateAnalysis(
        "health",
        healthResponse.data.result
      );

      setCurrentStep("Analysis completed.");

      navigate(
        `/project/project-${Date.now()}`
      );
    } catch (error) {
      console.error(error);

      const message =
        error?.response?.data?.detail ||
        error?.message ||
        "Something went wrong.";

      alert(message);
    } finally {
      setLoading(false);
      setAnalyzing(false);
    }
  };

  if (analyzing) {
    return (
      <LoadingAnalysis
        currentStep={currentStep}
      />
    );
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-8"
    >
      <div>
        <label className="mb-2 block text-sm font-medium text-slate-300">
          Project Name
        </label>

        <input
          type="text"
          value={form.name}
          onChange={(e) =>
            updateField("name", e.target.value)
          }
          placeholder="e.g. AI Project Intelligence System"
          className="
            w-full rounded-xl
            border border-slate-700
            bg-slate-900
            px-4 py-3
            text-white
            outline-none
            placeholder:text-slate-600
            focus:border-indigo-500
          "
        />
      </div>

      <div>
        <label className="mb-2 block text-sm font-medium text-slate-300">
          Project Description
        </label>

        <textarea
          rows={5}
          value={form.description}
          onChange={(e) =>
            updateField(
              "description",
              e.target.value
            )
          }
          placeholder="Describe your project, goals and expected outcomes..."
          className="
            w-full rounded-xl
            border border-slate-700
            bg-slate-900
            px-4 py-3
            text-white
            outline-none
            resize-none
            placeholder:text-slate-600
            focus:border-indigo-500
          "
        />
      </div>

      <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
        <div>
          <label className="mb-2 block text-sm font-medium text-slate-300">
            Start Date
          </label>

          <div className="relative">
            <Calendar
              size={18}
              className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500"
            />

            <input
              type="date"
              value={form.startDate}
              onChange={(e) =>
                updateField(
                  "startDate",
                  e.target.value
                )
              }
              className="
                w-full rounded-xl
                border border-slate-700
                bg-slate-900
                px-11 py-3
                text-white
                outline-none
                focus:border-indigo-500
              "
            />
          </div>
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-300">
            End Date
          </label>

          <div className="relative">
            <Calendar
              size={18}
              className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500"
            />

            <input
              type="date"
              value={form.endDate}
              onChange={(e) =>
                updateField(
                  "endDate",
                  e.target.value
                )
              }
              className="
                w-full rounded-xl
                border border-slate-700
                bg-slate-900
                px-11 py-3
                text-white
                outline-none
                focus:border-indigo-500
              "
            />
          </div>
        </div>
      </div>

      <div>
        <label className="mb-2 block text-sm font-medium text-slate-300">
          Project Status
        </label>

        <select
          value={form.status}
          onChange={(e) =>
            updateField("status", e.target.value)
          }
          className="
            w-full rounded-xl
            border border-slate-700
            bg-slate-900
            px-4 py-3
            text-white
            outline-none
            focus:border-indigo-500
          "
        >
          <option>Not Started</option>
          <option>In Progress</option>
          <option>On Hold</option>
          <option>Completed</option>
        </select>
      </div>

      <FileUpload
        files={files}
        setFiles={setFiles}
      />

      <button
        type="submit"
        className="
          flex w-full items-center
          justify-center gap-3
          rounded-xl
          bg-indigo-600
          px-6 py-4
          font-semibold text-white
          transition
          hover:bg-indigo-500
          disabled:cursor-not-allowed
          disabled:opacity-50
        "
      >
        <Sparkles size={20} />

        Analyze Project
      </button>
    </form>
  );
};

export default ProjectForm;