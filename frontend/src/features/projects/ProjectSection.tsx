import { Card } from "antd";

import { PROJECTS } from "../../app/constants";

export function ProjectSection() {
  return (
    <section id="projects" className="section-stack">
      <div className="section-head section-head-compact">
        <span className="section-chip">Projects</span>
        <h2>项目</h2>
      </div>

      <div className="project-grid">
        {PROJECTS.map((project, index) => (
          <Card
            key={project.title}
            className={index === 0 ? "panel-card project-card project-card-featured" : "panel-card project-card"}
            bordered={false}
          >
            <div className="project-card-head">
              <span className="project-index">{String(index + 1).padStart(2, "0")}</span>
              <div className="project-category">{project.category}</div>
            </div>
            <h3>{project.title}</h3>
            <p>{project.description}</p>
            <span className="project-meta">{project.meta}</span>
          </Card>
        ))}
      </div>
    </section>
  );
}
