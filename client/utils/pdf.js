import jsPDF from "jspdf";

const createPdf = (title, sections, fileName) => {
  const pdf = new jsPDF();

  const margin = 15;
  const pageWidth = pdf.internal.pageSize.getWidth();
  const pageHeight = pdf.internal.pageSize.getHeight();

  let y = 20;

  const addTitle = (text) => {
    pdf.setFontSize(18);
    pdf.setFont("helvetica", "bold");
    pdf.text(text, margin, y);
    y += 12;
  };

  const addText = (text, fontSize = 11) => {
    pdf.setFontSize(fontSize);
    pdf.setFont("helvetica", "normal");

    const lines = pdf.splitTextToSize(
      String(text || "Not specified"),
      pageWidth - margin * 2
    );

    for (const line of lines) {
      if (y > pageHeight - 20) {
        pdf.addPage();
        y = 20;
      }

      pdf.text(line, margin, y);
      y += 6;
    }

    y += 3;
  };

  const addHeading = (text) => {
    if (y > pageHeight - 30) {
      pdf.addPage();
      y = 20;
    }

    pdf.setFontSize(13);
    pdf.setFont("helvetica", "bold");
    pdf.text(text, margin, y);
    y += 8;
  };

  addTitle(title);

  sections.forEach((section) => {
    addHeading(section.heading);

    if (Array.isArray(section.items)) {
      section.items.forEach((item, index) => {
        addText(`${index + 1}. ${item}`);
      });
    } else {
      addText(section.content);
    }
  });

  pdf.save(fileName);
};


/* =========================
   USER STORIES
========================= */

export const downloadUserStoriesPdf = (stories = []) => {
  const items = stories.map((story, index) => {
    const id =
      story?.id ||
      story?.story_id ||
      `US-${String(index + 1).padStart(2, "0")}`;

    const description =
      story?.user_story ||
      story?.story ||
      story?.description ||
      story?.title ||
      JSON.stringify(story);

    const priority =
      story?.priority ||
      "Not specified";

    return `${id}
Priority: ${priority}
${description}`;
  });

  createPdf(
    "User Stories",
    [
      {
        heading: "Generated User Stories",
        items:
          items.length > 0
            ? items
            : ["No user stories generated."],
      },
    ],
    "user-stories.pdf"
  );
};


/* =========================
   RISK REGISTER
========================= */

export const downloadRiskRegisterPdf = (risks = []) => {
  const items = risks.map((risk, index) => {
    const name =
      risk?.risk ||
      risk?.title ||
      risk?.description ||
      `Risk ${index + 1}`;

    const impact =
      risk?.impact ||
      "Not specified";

    const likelihood =
      risk?.likelihood ||
      "Not specified";

    const owner =
      risk?.owner ||
      risk?.assignee ||
      risk?.assigned_to ||
      "Not specified";

    const mitigation =
      risk?.mitigation ||
      risk?.mitigation_strategy ||
      risk?.action ||
      "Not specified";

    return `Risk ${index + 1}: ${name}
Impact: ${impact}
Likelihood: ${likelihood}
Owner: ${owner}
Mitigation: ${mitigation}`;
  });

  createPdf(
    "Risk Register",
    [
      {
        heading: "Project Risks",
        items:
          items.length > 0
            ? items
            : ["No risks identified."],
      },
    ],
    "risk-register.pdf"
  );
};


/* =========================
   ACTION ITEMS
========================= */

export const downloadActionItemsPdf = (actions = []) => {
  const items = actions.map((action, index) => {
    const description =
      action?.action ||
      action?.action_item ||
      action?.description ||
      action?.task ||
      action?.title ||
      `Action Item ${index + 1}`;

    const owner =
      action?.owner ||
      action?.assignee ||
      action?.assigned_to ||
      "Not specified";

    const status =
      action?.status ||
      "Not specified";

    const dueDate =
      action?.due_date ||
      action?.deadline ||
      action?.date ||
      action?.dueDate ||
      "Not specified";

    return `Action Item ${index + 1}
${description}
Owner: ${owner}
Status: ${status}
Due Date: ${dueDate}`;
  });

  createPdf(
    "Action Items",
    [
      {
        heading: "Project Action Items",
        items:
          items.length > 0
            ? items
            : ["No action items generated."],
      },
    ],
    "action-items.pdf"
  );
};


/* =========================
   COMPLETE DOCUMENTATION
========================= */

export const downloadProjectDocumentationPdf = ({
  projectName = "AI Project Intelligence System",
  userStories = [],
  risks = [],
  actions = [],
  deliverables = [],
} = {}) => {
  const sections = [];

  sections.push({
    heading: "Project",
    content: projectName,
  });


  /* User Stories */

  const storyItems = userStories.map((story, index) => {
    const id =
      story?.id ||
      story?.story_id ||
      `US-${index + 1}`;

    const description =
      story?.user_story ||
      story?.story ||
      story?.description ||
      story?.title ||
      JSON.stringify(story);

    return `${id}: ${description}`;
  });

  sections.push({
    heading: "User Stories",
    items:
      storyItems.length > 0
        ? storyItems
        : ["No user stories generated."],
  });


  /* Risks */

  const riskItems = risks.map((risk, index) => {
    const name =
      risk?.risk ||
      risk?.title ||
      risk?.description ||
      `Risk ${index + 1}`;

    return `${name}
Impact: ${risk?.impact || "Not specified"}
Likelihood: ${risk?.likelihood || "Not specified"}
Owner: ${
      risk?.owner ||
      risk?.assignee ||
      risk?.assigned_to ||
      "Not specified"
    }
Mitigation: ${
      risk?.mitigation ||
      risk?.mitigation_strategy ||
      risk?.action ||
      "Not specified"
    }`;
  });

  sections.push({
    heading: "Risk Register",
    items:
      riskItems.length > 0
        ? riskItems
        : ["No risks identified."],
  });


  /* Action Items */

  const actionItems = actions.map((action, index) => {
    const description =
      action?.action ||
      action?.action_item ||
      action?.description ||
      action?.task ||
      action?.title ||
      `Action Item ${index + 1}`;

    return `${description}
Owner: ${
      action?.owner ||
      action?.assignee ||
      action?.assigned_to ||
      "Not specified"
    }
Status: ${action?.status || "Not specified"}
Due Date: ${
      action?.due_date ||
      action?.deadline ||
      action?.date ||
      action?.dueDate ||
      "Not specified"
    }`;
  });

  sections.push({
    heading: "Action Items",
    items:
      actionItems.length > 0
        ? actionItems
        : ["No action items generated."],
  });


  /* Deliverables */

  const deliverableItems = deliverables.map((item, index) => {
    const name =
      typeof item === "string"
        ? item
        : item?.milestone_name ||
          item?.name ||
          item?.deliverable ||
          item?.title ||
          `Deliverable ${index + 1}`;

    const description =
      typeof item === "string"
        ? ""
        : item?.description ||
          item?.details ||
          item?.summary ||
          "";

    const date =
      typeof item === "string"
        ? ""
        : item?.date ||
          item?.deadline ||
          item?.due_date ||
          item?.dueDate ||
          "";

    return `${name}
${description}
Date: ${date || "Not specified"}`;
  });

  sections.push({
    heading: "Deliverables & Milestones",
    items:
      deliverableItems.length > 0
        ? deliverableItems
        : ["No deliverables identified."],
  });


  createPdf(
    `${projectName} - Project Documentation`,
    sections,
    "project-documentation.pdf"
  );
};