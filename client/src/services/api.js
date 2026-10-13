import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL ||
    "http://localhost:8000",

  timeout: 120000,
});


/* ----------------------------------
   Upload Documents
---------------------------------- */

export const uploadDocuments = async (files) => {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  const response = await api.post(
    "/upload-multiple",
    formData
  );

  return response.data;
};


/* ----------------------------------
   Scope Agent
---------------------------------- */

export const runScopeAgent = async () => {
  const response = await api.post(
    "/agents/scope"
  );

  return response.data;
};


/* ----------------------------------
   Risk Agent
---------------------------------- */

export const runRiskAgent = async () => {
  const response = await api.post(
    "/agents/risk"
  );

  return response.data;
};


/* ----------------------------------
   Blocker Agent
---------------------------------- */

export const runBlockerAgent = async () => {
  const response = await api.post(
    "/agents/blocker"
  );

  return response.data;
};


/* ----------------------------------
   Documentation Agent
---------------------------------- */

export const runDocumentationAgent = async () => {
  const response = await api.post(
    "/agents/documentation"
  );

  return response.data;
};


/* ----------------------------------
   Project Health Agent
---------------------------------- */

export const runHealthAgent = async () => {
  const response = await api.post(
    "/agents/health"
  );

  return response.data;
};


/* ----------------------------------
   Project Assistant
---------------------------------- */

export const askAssistant = async (
  query,
  topK = 6
) => {
  const response = await api.post(
    "/assistant/ask",
    {
      query,
      top_k: topK,
    }
  );

  return response.data;
};


export default api;