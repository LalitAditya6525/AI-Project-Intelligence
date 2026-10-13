function BlockerPage({ data }) {

  const blockers =
    data?.blockers ||
    data?.issues ||
    [];

  const actions =
    data?.action_items ||
    data?.actions ||
    [];


  return (
    <div className="space-y-8">

      {/* Blockers */}

      <section>

        <div className="mb-5">

          <h1 className="text-2xl font-bold text-white">
            Blockers
          </h1>

          <p className="mt-2 text-sm text-gray-500">
            Current blockers and unresolved issues
            identified from project information.
          </p>

        </div>


        {Array.isArray(blockers) &&
        blockers.length > 0 ? (

          <div className="space-y-4">

            {blockers.map(
              (blocker, index) => (

                <div
                  key={index}
                  className="rounded-2xl border border-gray-800 bg-[#111722] p-5"
                >

                  <div className="flex gap-4">

                    <span className="text-xl">
                      🚧
                    </span>

                    <div>

                      <h3 className="font-medium text-white">
                        {blocker?.blocker ||
                          blocker?.issue ||
                          blocker?.description ||
                          `Blocker ${index + 1}`}
                      </h3>

                      {blocker?.owner && (

                        <p className="mt-2 text-sm text-gray-500">
                          Owner: {blocker.owner}
                        </p>

                      )}

                    </div>

                  </div>

                </div>

              )
            )}

          </div>

        ) : (

          <div className="rounded-2xl border border-gray-800 bg-[#111722] p-6 text-sm text-gray-500">
            No blocker information was returned.
          </div>

        )}

      </section>


      {/* Actions */}

      <section>

        <div className="mb-5">

          <h2 className="text-xl font-semibold text-white">
            Action Items
          </h2>

        </div>


        {Array.isArray(actions) &&
        actions.length > 0 ? (

          <div className="space-y-3">

            {actions.map(
              (action, index) => (

                <div
                  key={index}
                  className="rounded-xl border border-gray-800 bg-[#111722] p-5"
                >

                  <div className="flex items-start gap-4">

                    <span className="text-indigo-400">
                      ✓
                    </span>

                    <div>

                      <p className="text-sm text-gray-300">
                        {action?.action ||
                          action?.description ||
                          JSON.stringify(
                            action
                          )}
                      </p>

                      {action?.owner && (

                        <p className="mt-2 text-xs text-gray-600">
                          Owner: {action.owner}
                        </p>

                      )}

                    </div>

                  </div>

                </div>

              )
            )}

          </div>

        ) : (

          <div className="rounded-2xl border border-gray-800 bg-[#111722] p-6 text-sm text-gray-500">
            No action items returned.
          </div>

        )}

      </section>

    </div>
  );
}

export default BlockerPage;