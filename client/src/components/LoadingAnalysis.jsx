function LoadingAnalysis({ step }) {

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#0b0f17] px-6">

      <div className="w-full max-w-xl">

        <div className="mb-8 text-center">

          <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-2xl border border-indigo-500/20 bg-indigo-500/10 text-4xl">
            🤖
          </div>

          <h1 className="text-3xl font-bold text-white">
            Analyzing Your Project
          </h1>

          <p className="mt-3 text-gray-500">
            AI agents are analyzing your project documents.
          </p>

        </div>


        <div className="rounded-2xl border border-gray-800 bg-[#111722] p-6">

          <div className="mb-6 flex items-center gap-4">

            <div className="h-8 w-8 animate-spin rounded-full border-2 border-gray-700 border-t-indigo-500" />

            <div>

              <p className="text-sm font-medium text-white">
                Analysis in progress
              </p>

              <p className="mt-1 text-xs text-gray-500">
                {step}
              </p>

            </div>

          </div>


          <div className="space-y-3">

            {[
              "Document ingestion",
              "Scope & deliverable analysis",
              "Risk detection",
              "Blocker analysis",
              "Documentation generation",
              "Project health scoring",
            ].map((item) => (

              <div
                key={item}
                className="flex items-center gap-3 rounded-lg bg-[#0b0f17] px-4 py-3"
              >

                <div className="h-2 w-2 rounded-full bg-indigo-500" />

                <span className="text-sm text-gray-400">
                  {item}
                </span>

              </div>

            ))}

          </div>

        </div>

      </div>

    </div>
  );
}

export default LoadingAnalysis;