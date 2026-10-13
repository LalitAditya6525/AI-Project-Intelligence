import {
  AlertTriangle,
  CalendarDays,
  CheckCircle2,
  Download,
  FileText,
  ListChecks,
  ShieldAlert,
  Target,
  Users,
} from "lucide-react";

import {
  downloadUserStoriesPdf,
  downloadRiskRegisterPdf,
  downloadActionItemsPdf,
  downloadProjectDocumentationPdf,
} from "../../../utils/pdf.js";


function DocumentationPage({ data }) {
  /*
   * Supports both:
   *
   * {
   *   user_stories: [],
   *   risk_register: [],
   *   action_items: []
   * }
   *
   * and:
   *
   * {
   *   result: {
   *     user_stories: [],
   *     risk_register: [],
   *     action_items: []
   *   }
   * }
   */

  const result = data?.result || data || {};

  const projectName =
    result?.project_name ||
    result?.projectName ||
    "AI Project Intelligence System";

  /* =====================================================
     DATA
  ===================================================== */

  const userStories = Array.isArray(result?.user_stories)
    ? result.user_stories
    : Array.isArray(result?.userStories)
      ? result.userStories
      : [];

  const risks = Array.isArray(result?.risk_register)
    ? result.risk_register
    : Array.isArray(result?.riskRegister)
      ? result.riskRegister
      : Array.isArray(result?.risks)
        ? result.risks
        : [];

  const actions = Array.isArray(result?.action_items)
    ? result.action_items
    : Array.isArray(result?.actionItems)
      ? result.actionItems
      : [];

  const deliverables = Array.isArray(result?.deliverables)
    ? result.deliverables
    : Array.isArray(result?.milestones)
      ? result.milestones
      : Array.isArray(result?.major_deliverables)
        ? result.major_deliverables
        : [];


  /* =====================================================
     HELPERS
  ===================================================== */

  const getStoryText = (story) => {
    if (typeof story === "string") {
      return story;
    }

    return (
      story?.user_story ||
      story?.description ||
      story?.story ||
      story?.details ||
      "No description available."
    );
  };

  const getStoryTitle = (story, index) => {
    if (typeof story === "string") {
      return `User Story ${index + 1}`;
    }

    return (
      story?.title ||
      story?.name ||
      story?.feature ||
      story?.id ||
      `User Story ${index + 1}`
    );
  };


  const getRiskName = (risk, index) => {
    if (typeof risk === "string") {
      return risk;
    }

    return (
      risk?.risk ||
      risk?.title ||
      risk?.name ||
      `Risk ${index + 1}`
    );
  };


  const getRiskSeverity = (risk) => {
    if (typeof risk === "string") {
      return "";
    }

    return (
      risk?.severity ||
      risk?.priority ||
      risk?.level ||
      ""
    );
  };


  const getRiskDescription = (risk) => {
    if (typeof risk === "string") {
      return "";
    }

    return (
      risk?.description ||
      risk?.details ||
      risk?.summary ||
      ""
    );
  };


  const getActionText = (action) => {
    if (typeof action === "string") {
      return action;
    }

    return (
      action?.action ||
      action?.action_item ||
      action?.description ||
      action?.task ||
      action?.title ||
      "No action description available."
    );
  };


  const getActionOwner = (action) => {
    if (typeof action === "string") {
      return "";
    }

    return (
      action?.owner ||
      action?.assignee ||
      action?.assigned_to ||
      ""
    );
  };


  const getActionStatus = (action) => {
    if (typeof action === "string") {
      return "";
    }

    return action?.status || "";
  };


  const getActionDate = (action) => {
    if (typeof action === "string") {
      return "";
    }

    return (
      action?.due_date ||
      action?.dueDate ||
      action?.deadline ||
      action?.date ||
      ""
    );
  };


  const getDeliverableName = (item, index) => {
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


  const getDeliverableDescription = (item) => {
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


  const getDeliverableDate = (item) => {
    if (typeof item === "string") {
      return "";
    }

    return (
      item?.date ||
      item?.deadline ||
      item?.due_date ||
      item?.dueDate ||
      ""
    );
  };


  const formatDate = (date) => {
    if (!date) return "";

    const parsed = new Date(date);

    if (Number.isNaN(parsed.getTime())) {
      return date;
    }

    return parsed.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };


  /* =====================================================
     PDF HANDLERS
  ===================================================== */

  const downloadStories = () => {
    downloadUserStoriesPdf(
      userStories,
      projectName
    );
  };


  const downloadRisks = () => {
    downloadRiskRegisterPdf(
      risks,
      projectName
    );
  };


  const downloadActions = () => {
    downloadActionItemsPdf(
      actions,
      projectName
    );
  };


  const downloadCompleteDocumentation = () => {
    downloadProjectDocumentationPdf(
      result,
      projectName
    );
  };


  /* =====================================================
     PAGE
  ===================================================== */

  return (
    <div className="space-y-8 pb-12">

      {/* =================================================
          HEADER
      ================================================= */}

      <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">

        <div>

          <div className="flex items-center gap-3">

            <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-indigo-500/20 bg-indigo-500/10">
              <FileText
                size={23}
                className="text-indigo-400"
              />
            </div>

            <div>

              <h1 className="text-3xl font-bold tracking-tight text-white">
                Generated Documentation
              </h1>

              <p className="mt-2 text-sm text-gray-500">
                Structured project documentation generated
                from your uploaded project information.
              </p>

            </div>

          </div>

        </div>


        <button
          onClick={downloadCompleteDocumentation}
          className="flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 py-3 text-sm font-medium text-white transition hover:bg-indigo-500"
        >
          <Download size={17} />
          Download Complete PDF
        </button>

      </div>


      {/* =================================================
          SUMMARY CARDS
      ================================================= */}

      <div className="grid gap-4 sm:grid-cols-3">

        <SummaryCard
          icon={Users}
          label="User Stories"
          value={userStories.length}
          iconClass="text-indigo-400"
          bgClass="bg-indigo-500/10"
        />

        <SummaryCard
          icon={ShieldAlert}
          label="Risks"
          value={risks.length}
          iconClass="text-red-400"
          bgClass="bg-red-500/10"
        />

        <SummaryCard
          icon={ListChecks}
          label="Action Items"
          value={actions.length}
          iconClass="text-amber-400"
          bgClass="bg-amber-500/10"
        />

      </div>


      {/* =================================================
          USER STORIES
      ================================================= */}

      <section className="overflow-hidden rounded-2xl border border-gray-800 bg-[#111722]">

        <SectionHeader
          icon={Users}
          iconClass="text-indigo-400"
          iconBg="bg-indigo-500/10"
          title="User Stories"
          description="Requirements converted into actionable user stories."
          count={userStories.length}
          buttonText="Download PDF"
          onDownload={downloadStories}
          disabled={userStories.length === 0}
        />


        {userStories.length > 0 ? (

          <div className="divide-y divide-gray-800">

            {userStories.map((story, index) => (

              <div
                key={index}
                className="p-6 transition hover:bg-white/[0.015]"
              >

                <div className="flex gap-4">

                  {/* Number */}

                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-500/10 text-sm font-semibold text-indigo-400">
                    {String(index + 1).padStart(2, "0")}
                  </div>


                  {/* Content */}

                  <div className="min-w-0 flex-1">

                    <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">

                      <div>

                        <div className="flex items-center gap-2">

                          <span className="text-xs font-medium text-indigo-400">
                            {story?.id ||
                              story?.story_id ||
                              `US-${String(index + 1).padStart(2, "0")}`}
                          </span>

                        </div>

                        <h3 className="mt-1 text-base font-semibold text-white">
                          {getStoryTitle(
                            story,
                            index
                          )}
                        </h3>

                      </div>


                      {story?.priority && (
                        <PriorityBadge
                          priority={story.priority}
                        />
                      )}

                    </div>


                    <p className="mt-3 text-sm leading-7 text-gray-400">
                      {getStoryText(story)}
                    </p>


                    {story?.status && (
                      <div className="mt-4">

                        <StatusBadge
                          status={story.status}
                        />

                      </div>
                    )}

                  </div>

                </div>

              </div>

            ))}

          </div>

        ) : (

          <EmptyState
            icon={FileText}
            message="No user stories were generated."
          />

        )}

      </section>


      {/* =================================================
          RISK REGISTER
      ================================================= */}

      <section className="overflow-hidden rounded-2xl border border-gray-800 bg-[#111722]">

        <SectionHeader
          icon={ShieldAlert}
          iconClass="text-red-400"
          iconBg="bg-red-500/10"
          title="Risk Register"
          description="Identified project risks and their associated information."
          count={risks.length}
          buttonText="Download PDF"
          onDownload={downloadRisks}
          disabled={risks.length === 0}
        />


        {risks.length > 0 ? (

          <div className="divide-y divide-gray-800">

            {risks.map((risk, index) => (

              <div
                key={index}
                className="p-6"
              >

                <div className="flex gap-4">

                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-red-500/10">
                    <AlertTriangle
                      size={18}
                      className="text-red-400"
                    />
                  </div>


                  <div className="min-w-0 flex-1">

                    <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">

                      <div>

                        <span className="text-xs text-gray-600">
                          RISK-{String(index + 1).padStart(2, "0")}
                        </span>

                        <h3 className="mt-1 font-semibold text-white">
                          {getRiskName(
                            risk,
                            index
                          )}
                        </h3>

                      </div>


                      {getRiskSeverity(risk) && (
                        <RiskBadge
                          severity={getRiskSeverity(
                            risk
                          )}
                        />
                      )}

                    </div>


                    {getRiskDescription(risk) && (
                      <p className="mt-3 text-sm leading-6 text-gray-400">
                        {getRiskDescription(risk)}
                      </p>
                    )}


                    <div className="mt-5 grid gap-3 sm:grid-cols-3">

                      <InfoBox
                        label="Impact"
                        value={
                          risk?.impact ||
                          "Not specified"
                        }
                      />

                      <InfoBox
                        label="Likelihood"
                        value={
                          risk?.likelihood ||
                          "Not specified"
                        }
                      />

                      <InfoBox
                        label="Owner"
                        value={
                          risk?.owner ||
                          risk?.assignee ||
                          "Not specified"
                        }
                      />

                    </div>


                    {(risk?.mitigation ||
                      risk?.mitigation_plan ||
                      risk?.recommendation) && (

                      <div className="mt-4 rounded-xl border border-gray-800 bg-[#0b0f17] p-4">

                        <p className="text-xs font-semibold uppercase tracking-wider text-gray-600">
                          Mitigation
                        </p>

                        <p className="mt-2 text-sm leading-6 text-gray-400">
                          {risk?.mitigation ||
                            risk?.mitigation_plan ||
                            risk?.recommendation}
                        </p>

                      </div>

                    )}

                  </div>

                </div>

              </div>

            ))}

          </div>

        ) : (

          <EmptyState
            icon={CheckCircle2}
            message="No risks were identified."
          />

        )}

      </section>


      {/* =================================================
          ACTION ITEMS
      ================================================= */}

      <section className="overflow-hidden rounded-2xl border border-gray-800 bg-[#111722]">

        <SectionHeader
          icon={ListChecks}
          iconClass="text-amber-400"
          iconBg="bg-amber-500/10"
          title="Action Items"
          description="Actions extracted from requirements, meetings and project updates."
          count={actions.length}
          buttonText="Download PDF"
          onDownload={downloadActions}
          disabled={actions.length === 0}
        />


        {actions.length > 0 ? (

          <div className="divide-y divide-gray-800">

            {actions.map((action, index) => (

              <div
                key={index}
                className="p-6"
              >

                <div className="flex gap-4">

                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-amber-500/10">
                    <ListChecks
                      size={18}
                      className="text-amber-400"
                    />
                  </div>


                  <div className="min-w-0 flex-1">

                    <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">

                      <div>

                        <span className="text-xs text-gray-600">
                          ACTION-{String(index + 1).padStart(2, "0")}
                        </span>

                        <p className="mt-1 text-sm font-medium leading-6 text-gray-200">
                          {getActionText(action)}
                        </p>

                      </div>


                      {getActionStatus(action) && (
                        <StatusBadge
                          status={getActionStatus(
                            action
                          )}
                        />
                      )}

                    </div>


                    <div className="mt-4 flex flex-wrap gap-2">

                      {getActionOwner(action) && (
                        <span className="rounded-lg border border-gray-800 bg-[#0b0f17] px-3 py-1.5 text-xs text-gray-500">

                          Owner:{" "}

                          <span className="text-gray-300">
                            {getActionOwner(action)}
                          </span>

                        </span>
                      )}


                      {getActionDate(action) && (
                        <span className="flex items-center gap-1.5 rounded-lg border border-gray-800 bg-[#0b0f17] px-3 py-1.5 text-xs text-gray-500">

                          <CalendarDays
                            size={13}
                          />

                          {formatDate(
                            getActionDate(action)
                          )}

                        </span>
                      )}

                    </div>

                  </div>

                </div>

              </div>

            ))}

          </div>

        ) : (

          <EmptyState
            icon={CheckCircle2}
            message="No action items were generated."
          />

        )}

      </section>


      {/* =================================================
          DELIVERABLES
      ================================================= */}

      <section className="overflow-hidden rounded-2xl border border-gray-800 bg-[#111722]">

        <div className="flex items-center gap-4 border-b border-gray-800 p-6">

          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-500/10">

            <Target
              size={20}
              className="text-emerald-400"
            />

          </div>

          <div>

            <h2 className="text-lg font-semibold text-white">
              Deliverables & Milestones
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Major outputs and milestones identified from the project.
            </p>

          </div>

        </div>


        {deliverables.length > 0 ? (

          <div className="divide-y divide-gray-800">

            {deliverables.map((item, index) => (

              <div
                key={index}
                className="flex gap-4 p-6"
              >

                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-500/10 text-sm font-semibold text-emerald-400">
                  {String(index + 1).padStart(2, "0")}
                </div>


                <div className="flex-1">

                  <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">

                    <div>

                      <h3 className="font-semibold text-white">
                        {getDeliverableName(
                          item,
                          index
                        )}
                      </h3>

                      {getDeliverableDescription(
                        item
                      ) && (

                        <p className="mt-2 text-sm leading-6 text-gray-400">
                          {getDeliverableDescription(
                            item
                          )}
                        </p>

                      )}

                    </div>


                    {getDeliverableDate(item) && (

                      <span className="flex shrink-0 items-center gap-2 rounded-lg border border-gray-800 bg-[#0b0f17] px-3 py-2 text-xs text-gray-400">

                        <CalendarDays
                          size={14}
                          className="text-emerald-400"
                        />

                        {formatDate(
                          getDeliverableDate(item)
                        )}

                      </span>

                    )}

                  </div>

                </div>

              </div>

            ))}

          </div>

        ) : (

          <EmptyState
            icon={CalendarDays}
            message="No deliverables or milestones were generated."
          />

        )}

      </section>


      {/* =================================================
          FOOTER
      ================================================= */}

      <div className="flex flex-col gap-4 rounded-2xl border border-indigo-500/10 bg-indigo-500/[0.03] p-6 sm:flex-row sm:items-center sm:justify-between">

        <div>

          <h3 className="font-semibold text-white">
            Documentation Ready
          </h3>

          <p className="mt-1 text-sm text-gray-500">
            Download the complete generated documentation
            for project records and reporting.
          </p>

        </div>


        <button
          onClick={downloadCompleteDocumentation}
          className="flex shrink-0 items-center justify-center gap-2 rounded-lg border border-gray-700 bg-[#111722] px-4 py-2.5 text-sm font-medium text-gray-300 transition hover:border-indigo-500/40 hover:text-white"
        >
          <Download size={16} />
          Export Documentation
        </button>

      </div>

    </div>
  );
}


/* =========================================================
   SECTION HEADER
========================================================= */

function SectionHeader({
  icon: Icon,
  iconClass,
  iconBg,
  title,
  description,
  count,
  buttonText,
  onDownload,
  disabled,
}) {
  return (
    <div className="flex flex-col gap-4 border-b border-gray-800 p-6 sm:flex-row sm:items-center sm:justify-between">

      <div className="flex items-center gap-4">

        <div
          className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl ${iconBg}`}
        >
          <Icon
            size={20}
            className={iconClass}
          />
        </div>

        <div>

          <div className="flex items-center gap-3">

            <h2 className="text-lg font-semibold text-white">
              {title}
            </h2>

            <span className="rounded-full border border-gray-800 bg-[#0b0f17] px-2.5 py-1 text-xs text-gray-500">
              {count}
            </span>

          </div>

          <p className="mt-1 text-sm text-gray-500">
            {description}
          </p>

        </div>

      </div>


      <button
        onClick={onDownload}
        disabled={disabled}
        className="flex shrink-0 items-center justify-center gap-2 rounded-lg border border-gray-700 bg-[#0b0f17] px-4 py-2.5 text-sm font-medium text-gray-300 transition hover:border-indigo-500/40 hover:text-white disabled:cursor-not-allowed disabled:opacity-30"
      >
        <Download size={16} />
        {buttonText}
      </button>

    </div>
  );
}


/* =========================================================
   SUMMARY CARD
========================================================= */

function SummaryCard({
  icon: Icon,
  label,
  value,
  iconClass,
  bgClass,
}) {
  return (
    <div className="rounded-2xl border border-gray-800 bg-[#111722] p-5">

      <div className="flex items-center gap-4">

        <div
          className={`flex h-10 w-10 items-center justify-center rounded-xl ${bgClass}`}
        >
          <Icon
            size={19}
            className={iconClass}
          />
        </div>

        <div>

          <p className="text-2xl font-bold text-white">
            {value}
          </p>

          <p className="mt-1 text-xs text-gray-500">
            {label}
          </p>

        </div>

      </div>

    </div>
  );
}


/* =========================================================
   INFO BOX
========================================================= */

function InfoBox({
  label,
  value,
}) {
  return (
    <div className="rounded-xl border border-gray-800 bg-[#0b0f17] p-3">

      <p className="text-[11px] font-medium uppercase tracking-wider text-gray-600">
        {label}
      </p>

      <p className="mt-1 text-sm text-gray-400">
        {value}
      </p>

    </div>
  );
}


/* =========================================================
   PRIORITY BADGE
========================================================= */

function PriorityBadge({
  priority,
}) {
  const value = String(priority).toLowerCase();

  let classes =
    "border-gray-700 bg-gray-800/50 text-gray-400";

  if (value === "high" || value === "critical") {
    classes =
      "border-red-500/20 bg-red-500/5 text-red-400";
  } else if (value === "medium") {
    classes =
      "border-amber-500/20 bg-amber-500/5 text-amber-400";
  } else if (value === "low") {
    classes =
      "border-emerald-500/20 bg-emerald-500/5 text-emerald-400";
  }

  return (
    <span
      className={`w-fit rounded-full border px-3 py-1 text-xs font-medium ${classes}`}
    >
      {priority}
    </span>
  );
}


/* =========================================================
   RISK BADGE
========================================================= */

function RiskBadge({
  severity,
}) {
  const value = String(severity).toLowerCase();

  let classes =
    "border-gray-700 bg-gray-800/50 text-gray-400";

  if (
    value.includes("critical") ||
    value.includes("high")
  ) {
    classes =
      "border-red-500/20 bg-red-500/5 text-red-400";
  } else if (value.includes("medium")) {
    classes =
      "border-amber-500/20 bg-amber-500/5 text-amber-400";
  } else if (value.includes("low")) {
    classes =
      "border-emerald-500/20 bg-emerald-500/5 text-emerald-400";
  }

  return (
    <span
      className={`w-fit rounded-full border px-3 py-1 text-xs font-medium ${classes}`}
    >
      {severity}
    </span>
  );
}


/* =========================================================
   STATUS BADGE
========================================================= */

function StatusBadge({
  status,
}) {
  const value = String(status).toLowerCase();

  let classes =
    "border-gray-700 bg-gray-800/50 text-gray-400";

  if (
    value.includes("complete") ||
    value.includes("done") ||
    value.includes("closed")
  ) {
    classes =
      "border-emerald-500/20 bg-emerald-500/5 text-emerald-400";
  } else if (
    value.includes("pending") ||
    value.includes("progress")
  ) {
    classes =
      "border-amber-500/20 bg-amber-500/5 text-amber-400";
  } else if (
    value.includes("blocked") ||
    value.includes("failed")
  ) {
    classes =
      "border-red-500/20 bg-red-500/5 text-red-400";
  }

  return (
    <span
      className={`inline-flex rounded-full border px-3 py-1 text-xs font-medium ${classes}`}
    >
      {status}
    </span>
  );
}


/* =========================================================
   EMPTY STATE
========================================================= */

function EmptyState({
  icon: Icon,
  message,
}) {
  return (
    <div className="flex flex-col items-center justify-center px-6 py-14 text-center">

      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gray-800/70">

        <Icon
          size={20}
          className="text-gray-600"
        />

      </div>

      <p className="mt-4 text-sm text-gray-500">
        {message}
      </p>

    </div>
  );
}


export default DocumentationPage;