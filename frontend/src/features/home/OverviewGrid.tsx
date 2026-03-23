import { OVERVIEW_ITEMS } from "../../app/constants";

type OverviewGridProps = {
  onNavigate: (path: string) => void;
};

export function OverviewGrid({ onNavigate }: OverviewGridProps) {
  return (
    <section className="overview-grid">
      {OVERVIEW_ITEMS.map((item) => (
        <button
          key={item.title}
          type="button"
          className="overview-panel"
          onClick={() => onNavigate(item.path)}
        >
          <div className="overview-panel-head">
            <span className="section-chip">{item.label}</span>
          </div>
          <strong className="overview-panel-title">{item.title}</strong>
          <p>{item.description}</p>
          <span className="overview-panel-foot">进入</span>
        </button>
      ))}
    </section>
  );
}
