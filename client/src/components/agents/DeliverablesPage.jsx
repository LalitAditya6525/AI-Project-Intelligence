import {
  CalendarDays,
  CheckCircle2,
  Circle,
} from "lucide-react";

function DeliverablesPage({ data }) {

  const result = data?.result || data || {};

  const deliverables =
    result?.deliverables ||
    result?.milestones ||
    result?.major_deliverables ||
    [];


  const formatDate = (date) => {

    if (!date) return null;

    const parsedDate = new Date(date);

    if (Number.isNaN(parsedDate.getTime())) {
      return date;
    }

    return parsedDate.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };


  const getName = (item, index) => {

    if (typeof item === "string") {
      return item;
    }

    return (
      item?.milestone_name ||
      item?.name ||
      item?.deliverable ||
      item?.title ||
      `Deliverable ${index + 1}`
    );
  };


  const getDescription = (item) => {

    if (typeof item === "string") {
      return "";
    }

    return (
      item?.description ||
      item?.details ||
      item?.summary ||
      ""
    );
  };


  const getDate = (item) => {

    if (typeof item === "string") {
      return null;
    }

    return (
      item?.date ||
      item?.deadline ||
      item?.due_date ||
      item?.dueDate ||
      null
    );
  };


  return (
    <div className="space-y-8">

      {/* Header */}
      <div className="flex items-start justify-between">

        <div>

          <h1 className="text-3xl font-bold text-white">
            Deliverables & Milestones
          </h1>

          <p className="mt-2 text-gray-500">
            Project deliverables, milestones and deadlines
            identified from the uploaded documents.
          </p>

        </div>

        <div className="rounded-full border border-emerald-500/20 bg-emerald-500/5 px-4 py-2 text-sm text-emerald-400">
          Analysis Complete
        </div>

      </div>


      {/* Deliverables */}
      {Array.isArray(deliverables) &&
        deliverables.length > 0 ? (

        <div className="space-y-4">

          {deliverables.map((item, index) => {

            const name = getName(item, index);
            const description = getDescription(item);
            const date = getDate(item);

            return (
              <div
                key={index}
                className="rounded-2xl border border-gray-800 bg-[#111722] p-6 transition hover:border-indigo-500/30"
              >

                <div className="flex gap-5">

                  {/* Number */}
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-indigo-500/10 text-lg font-medium text-indigo-400">
                    {String(index + 1).padStart(2, "0")}
                  </div>


                  {/* Content */}
                  <div className="min-w-0 flex-1">

                    <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">

                      <div>

                        <h3 className="text-lg font-semibold text-white">
                          {name}
                        </h3>

                        {description && (
                          <p className="mt-2 text-sm leading-6 text-gray-400">
                            {description}
                          </p>
                        )}

                      </div>


                      {/* Date */}
                      {date && (
                        <div className="flex shrink-0 items-center gap-2 rounded-lg border border-gray-800 bg-[#0b0f17] px-3 py-2">

                          <CalendarDays
                            size={16}
                            className="text-indigo-400"
                          />

                          <span className="text-sm text-gray-300">
                            {formatDate(date)}
                          </span>

                        </div>
                      )}

                    </div>


                    {/* Status */}
                    <div className="mt-5 flex items-center gap-2">

                      <Circle
                        size={9}
                        className="fill-indigo-400 text-indigo-400"
                      />

                      <span className="text-xs text-gray-500">
                        Project milestone
                      </span>

                    </div>

                  </div>

                </div>

              </div>
            );
          })}

        </div>

      ) : (

        <div className="rounded-2xl border border-gray-800 bg-[#111722] p-7">

          <div className="flex items-center gap-3">

            <CheckCircle2
              size={20}
              className="text-gray-600"
            />

            <p className="text-sm text-gray-500">
              No deliverables or milestones were identified.
            </p>

          </div>

        </div>

      )}

    </div>
  );
}

export default DeliverablesPage;