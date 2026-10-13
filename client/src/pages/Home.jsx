import { useState } from "react";

import FileUpload from "../components/FileUpload";
import LoadingAnalysis from "../components/LoadingAnalysis";

import {
  uploadDocuments,
  runScopeAgent,
  runRiskAgent,
  runBlockerAgent,
  runDocumentationAgent,
  runHealthAgent,
} from "../services/api";


function Home({
  onProjectCreated,
}) {

  const [projectName, setProjectName] = useState("");
  const [description, setDescription] = useState("");

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const [files, setFiles] = useState([]);

  const [loading, setLoading] = useState(false);

  const [analysisStep, setAnalysisStep] =
    useState("");

  const [error, setError] = useState("");


  const startAnalysis = async (event) => {

    event.preventDefault();

    setError("");


    /* Validation */

    if (!projectName.trim()) {
      setError("Please enter a project name.");
      return;
    }

    if (!description.trim()) {
      setError(
        "Please enter a project description."
      );
      return;
    }

    if (files.length === 0) {
      setError(
        "Please upload at least one project document."
      );
      return;
    }


    try {

      setLoading(true);


      /* ------------------------------
         STEP 1
         Upload documents
      ------------------------------ */

      setAnalysisStep(
        "Uploading project documents..."
      );

      const uploadResult =
        await uploadDocuments(files);


      /* ------------------------------
         STEP 2
         Scope
      ------------------------------ */

      setAnalysisStep(
        "Scope Agent is analyzing your project..."
      );

      const scopeResult =
        await runScopeAgent();


      /* ------------------------------
         STEP 3
         Risk
      ------------------------------ */

      setAnalysisStep(
        "Risk Agent is detecting project risks..."
      );

      const riskResult =
        await runRiskAgent();


      /* ------------------------------
         STEP 4
         Blockers
      ------------------------------ */

      setAnalysisStep(
        "Blocker Agent is identifying blockers..."
      );

      const blockerResult =
        await runBlockerAgent();


      /* ------------------------------
         STEP 5
         Documentation
      ------------------------------ */

      setAnalysisStep(
        "Documentation Agent is generating project documentation..."
      );

      const documentationResult =
        await runDocumentationAgent();


      /* ------------------------------
         STEP 6
         Health
      ------------------------------ */

      setAnalysisStep(
        "Health Agent is calculating project health..."
      );

      const healthResult =
        await runHealthAgent();


      /* ------------------------------
         Store project
      ------------------------------ */

      const projectData = {

        id: Date.now(),

        name: projectName,

        description,

        startDate,

        endDate,

        files: files.map(
          (file) => file.name
        ),

        uploadResult,

        analysis: {

          scope:
            scopeResult?.result || {},

          risk:
            riskResult?.result || {},

          blocker:
            blockerResult?.result || {},

          documentation:
            documentationResult?.result || {},

          health:
            healthResult?.result || {},

        },

      };


      setAnalysisStep(
        "Analysis completed. Opening dashboard..."
      );


      /*
       * Small delay so the user can
       * see the completion message.
       */

      await new Promise(
        (resolve) =>
          setTimeout(resolve, 700)
      );


      onProjectCreated(projectData);


    } catch (err) {

      console.error(err);

      setError(
        err.message ||
        "Project analysis failed."
      );

    } finally {

      setLoading(false);

    }

  };


  if (loading) {

    return (
      <LoadingAnalysis
        step={analysisStep}
      />
    );

  }


  return (
    <div className="min-h-screen bg-[#0b0f17]">

      {/* Header */}

      <header className="border-b border-gray-800">

        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">

          <div>

            <h1 className="text-xl font-semibold text-white">
              AI Project Intelligence
            </h1>

            <p className="mt-1 text-xs text-gray-500">
              Project Intelligence & Risk Advisor
            </p>

          </div>

          <div className="rounded-full border border-gray-800 px-4 py-2 text-xs text-gray-500">
            AI-Powered Analysis
          </div>

        </div>

      </header>


      {/* Main */}

      <main className="flex min-h-[calc(100vh-81px)] justify-center px-6 py-12">

        <div className="w-full max-w-4xl">

          {/* Hero */}

          <div className="mb-10 text-center">

            <div className="mb-5 inline-flex rounded-full border border-indigo-500/20 bg-indigo-500/10 px-4 py-2 text-xs font-medium text-indigo-400">
              PROJECT INTELLIGENCE
            </div>

            <h2 className="text-4xl font-bold tracking-tight text-white md:text-5xl">
              Understand your project
              <span className="block text-indigo-400">
                with AI
              </span>
            </h2>

            <p className="mx-auto mt-4 max-w-2xl text-gray-500">
              Upload your project documents and let AI
              identify scope, deliverables, risks, blockers
              and overall project health.
            </p>

          </div>


          {/* Form */}

          <form
            onSubmit={startAnalysis}
            className="rounded-2xl border border-gray-800 bg-[#111722] p-6 shadow-2xl md:p-8"
          >

            {/* Project name */}

            <div className="mb-6">

              <label className="mb-2 block text-sm font-medium text-gray-300">
                Project Name
              </label>

              <input
                type="text"
                value={projectName}
                onChange={(event) =>
                  setProjectName(
                    event.target.value
                  )
                }
                placeholder="e.g. AI Project Intelligence System"
                className="w-full rounded-xl border border-gray-700 bg-[#0b0f17] px-4 py-3 text-white outline-none transition placeholder:text-gray-700 focus:border-indigo-500"
              />

            </div>


            {/* Description */}

            <div className="mb-6">

              <label className="mb-2 block text-sm font-medium text-gray-300">
                Project Description
              </label>

              <textarea
                value={description}
                onChange={(event) =>
                  setDescription(
                    event.target.value
                  )
                }
                rows={5}
                placeholder="Describe the project, objectives, current progress and important context..."
                className="w-full resize-none rounded-xl border border-gray-700 bg-[#0b0f17] px-4 py-3 text-white outline-none transition placeholder:text-gray-700 focus:border-indigo-500"
              />

            </div>


            {/* Dates */}

            <div className="mb-6 grid grid-cols-1 gap-5 md:grid-cols-2">

              <div>

                <label className="mb-2 block text-sm font-medium text-gray-300">
                  Start Date
                </label>

                <input
                  type="date"
                  value={startDate}
                  onChange={(event) =>
                    setStartDate(
                      event.target.value
                    )
                  }
                  className="w-full rounded-xl border border-gray-700 bg-[#0b0f17] px-4 py-3 text-white outline-none focus:border-indigo-500"
                />

              </div>


              <div>

                <label className="mb-2 block text-sm font-medium text-gray-300">
                  End Date
                </label>

                <input
                  type="date"
                  value={endDate}
                  onChange={(event) =>
                    setEndDate(
                      event.target.value
                    )
                  }
                  className="w-full rounded-xl border border-gray-700 bg-[#0b0f17] px-4 py-3 text-white outline-none focus:border-indigo-500"
                />

              </div>

            </div>


            {/* Files */}

            <div className="mb-6">

              <FileUpload
                files={files}
                setFiles={setFiles}
              />

            </div>


            {/* Error */}

            {error && (

              <div className="mb-6 rounded-xl border border-red-900/50 bg-red-950/20 px-4 py-3 text-sm text-red-400">
                {error}
              </div>

            )}


            {/* Submit */}

            <button
              type="submit"
              className="w-full rounded-xl bg-indigo-600 px-6 py-4 font-semibold text-white shadow-lg shadow-indigo-900/20 transition hover:bg-indigo-500"
            >
              Start Project Analysis
              <span className="ml-2">
                →
              </span>
            </button>

          </form>


          <p className="mt-6 text-center text-xs text-gray-700">
            Supported formats: PDF · DOCX · CSV · TXT
          </p>

        </div>

      </main>

    </div>
  );
}

export default Home;