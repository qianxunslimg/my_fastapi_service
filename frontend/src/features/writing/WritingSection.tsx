import { Card } from "antd";

import { WRITING_ITEMS } from "../../app/constants";

export function WritingSection() {
  return (
    <section className="section-stack">
      <div className="section-head section-head-compact">
        <span className="section-chip">Writing</span>
        <h2>写作</h2>
      </div>

      <div className="writing-list">
        {WRITING_ITEMS.map((item, index) => (
          <Card key={item.title} className="panel-card writing-card" bordered={false}>
            <div className="writing-card-head">
              <span className="writing-category">{item.category}</span>
              <span className="writing-index">{String(index + 1).padStart(2, "0")}</span>
            </div>
            <h3>{item.title}</h3>
            <p>{item.summary}</p>
            <span className="writing-meta">{item.meta}</span>
          </Card>
        ))}
      </div>
    </section>
  );
}
