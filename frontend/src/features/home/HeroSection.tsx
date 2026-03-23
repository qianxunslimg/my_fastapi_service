import { Button } from "antd";

import { FEATURE_PILLS, HERO_NOTES } from "../../app/constants";

type HeroSectionProps = {
  onJumpToTool: () => void;
  onJumpToProjects: () => void;
};

export function HeroSection({ onJumpToTool, onJumpToProjects }: HeroSectionProps) {
  return (
    <section className="hero-layout">
      <article className="panel-card hero-primary">
        <div className="hero-top">
          <p className="eyebrow">PERSONAL SITE</p>
          <span className="hero-status">FastAPI + React</span>
        </div>

        <div className="hero-visual">
          <span className="hero-orbit hero-orbit-one" />
          <span className="hero-orbit hero-orbit-two" />
          <span className="hero-orbit hero-orbit-three" />
          <span className="hero-dot" />
        </div>

        <div className="hero-body">
          <p className="hero-kicker">projects / writing / tools</p>
          <h1>把个人站做成自己的工作台。</h1>
          <p className="hero-summary">项目、写作、工具放进同一个系统里，既能展示，也能直接开工。</p>
          <div className="hero-actions">
            <Button type="primary" size="large" onClick={onJumpToTool}>
              打开工具
            </Button>
            <Button size="large" onClick={onJumpToProjects}>
              看项目
            </Button>
          </div>
        </div>

        <div className="hero-pills">
          {FEATURE_PILLS.map((item) => (
            <span key={item} className="hero-pill">
              {item}
            </span>
          ))}
        </div>
      </article>

      <div className="hero-stack">
        {HERO_NOTES.map((item) => (
          <article key={item.label} className="panel-card hero-note">
            <span className="hero-note-label">{item.label}</span>
            <strong>{item.title}</strong>
            <p>{item.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
