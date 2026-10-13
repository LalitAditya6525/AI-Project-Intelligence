function RiskPage({ data }) {

  const risks =
    data?.risks ||
    data?.risk_register ||
    [];


  return (
    <div className="space-y-6">

      <div>

        <h1 className="text-2xl font-bold text-white">
          Risk Analysis
        </h1>

        <p className="mt-2 text-sm text-gray-500">
          Risks and delivery challenges identified by
          the Risk Detection Agent.
        </p>

      </div>


      {Array.isArray(risks) &&
      risks.length > 0 ? (

        <div className="grid gap-4">

          {risks.map(
            (risk, index) => (

              <div
                key={index}
                className="rounded-2xl border border-gray-800 bg-[#111722] p-6"
              >

                <div className="flex items-start justify-between gap-4">

                  <div>

                    <div className="flex items-center gap-3">

                      <span className="text-xl">
                        ⚠️
                      </span>

                      <h3 className="font-semibold text-white">
                        {risk?.risk ||
                          risk?.description ||
                          `Risk ${index + 1}`}
                      </h3>

                    </div>

                  </div>


                  {risk?.impact && (

                    <span className="rounded-full border border-yellow-500/20 bg-yellow-500/10 px-3 py-1 text-xs text-yellow-400">
                      {risk.impact}
                    </span>

                  )}

                </div>


                <div className="mt-5 grid gap-4 md:grid-cols-2">

                  {risk?.likelihood && (

                    <div>

                      <p className="text-xs uppercase text-gray-600">
                        Likelihood
                      </p>

                      <p className="mt-1 text-sm text-gray-300">
                        {risk.likelihood}
                      </p>

                    </div>

                  )}


                  {risk?.owner && (

                    <div>

                      <p className="text-xs uppercase text-gray-600">
                        Owner
                      </p>

                      <p className="mt-1 text-sm text-gray-300">
                        {risk.owner}
                      </p>

                    </div>

                  )}

                </div>


                {risk?.mitigation && (

                  <div className="mt-5 rounded-xl bg-[#0b0f17] p-4">

                    <p className="text-xs uppercase text-gray-600">
                      Mitigation
                    </p>

                    <p className="mt-2 text-sm leading-6 text-gray-400">
                      {risk.mitigation}
                    </p>

                  </div>

                )}

              </div>

            )
          )}

        </div>

      ) : (

        <div className="rounded-2xl border border-gray-800 bg-[#111722] p-6">

          <pre className="overflow-auto whitespace-pre-wrap text-sm text-gray-400">
            {JSON.stringify(
              data,
              null,
              2
            )}
          </pre>

        </div>

      )}

    </div>
  );
}

export default RiskPage;