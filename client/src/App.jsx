import { useState } from "react";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import {
  ProjectProvider,
  useProject,
} from "./context/ProjectContext";

function AppContent() {
  const [activeProject, setActiveProject] = useState(null);
  const { setProject, clearProject } = useProject();

  const handleProjectCreated = (projectData) => {
    setProject(projectData);
    setActiveProject(projectData);
  };

  const handleNewProject = () => {
    clearProject();
    setActiveProject(null);
  };

  return (
    <div className="min-h-screen bg-[#070d19] text-white">
      {activeProject ? (
        <Dashboard
          project={activeProject}
          onNewProject={handleNewProject}
        />
      ) : (
        <Home onProjectCreated={handleProjectCreated} />
      )}
    </div>
  );
}

export default function App() {
  return (
    <ProjectProvider>
      <AppContent />
    </ProjectProvider>
  );
}