import React, { createContext, useContext, useState } from 'react';

const ProjectContext = createContext();

export function ProjectProvider({ children }) {
  const [project, setProject] = useState(null);
  return (
    <ProjectContext.Provider value={{ project, setProject }}>
      {children}
    </ProjectContext.Provider>
  );
}

export function useProject() {
  return useContext(ProjectContext);
}
