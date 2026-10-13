import { createContext, useContext, useState } from "react";

const ProjectContext = createContext(null);

export function ProjectProvider({ children }) {
  const [project, setProject] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [analysis, setAnalysis] = useState({
    scope: null,
    risk: null,
    blocker: null,
    deliverables: null,
    documentation: null,
    health: null,
  });
  const [activePage, setActivePage] = useState("health");
  const [loading, setLoading] = useState(false);

  const updateAnalysis = (key, result) => {
    setAnalysis((previous) => ({
      ...previous,
      [key]: result,
    }));
  };

  const clearProject = () => {
    setProject(null);
    setDocuments([]);
    setAnalysis({
      scope: null,
      risk: null,
      blocker: null,
      deliverables: null,
      documentation: null,
      health: null,
    });
    setActivePage("health");
    setLoading(false);
  };

  return (
    <ProjectContext.Provider
      value={{
        project,
        setProject,
        documents,
        setDocuments,
        analysis,
        setAnalysis,
        updateAnalysis,
        activePage,
        setActivePage,
        loading,
        setLoading,
        clearProject,
      }}
    >
      {children}
    </ProjectContext.Provider>
  );
}

export function useProject() {
  const context = useContext(ProjectContext);

  if (!context) {
    throw new Error(
      "useProject must be used inside ProjectProvider"
    );
  }

  return context;
}
