import { Card } from "antd";

import { OVERVIEW_ITEMS } from "../../app/constants";

export function OverviewGrid() {
  return (
    <section className="overview-grid">
      {OVERVIEW_ITEMS.map((item, index) => (
        <Card
          key={item.title}
          className="panel-card overview-card"
          bordered={false}
        >
          <div className="overview-card-head">
            <span className="section-chip">{item.label}</span>
            <span className="overview-index">{String(index + 1).padStart(2, "0")}</span>
          </div>
          <h2>{item.title}</h2>
          <p>{item.description}</p>
        </Card>
      ))}
    </section>
  );
}
