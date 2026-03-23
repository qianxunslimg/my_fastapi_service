import { TOOLKIT_TABS } from "../../app/constants";
import { buildToolkitPath } from "../../app/routes";
import type { ToolkitTabKey } from "../../app/types";
import { SubTabBar } from "../../components/SubTabBar";
import { ToolkitSection } from "./ToolkitSection";

type ToolkitPageProps = {
  activeTab: ToolkitTabKey;
  onNavigate: (path: string) => void;
};

export function ToolkitPage({ activeTab, onNavigate }: ToolkitPageProps) {
  return (
    <div className="page-stack">
      <div className="page-head">
        <div className="section-head section-head-compact">
          <span className="section-chip">Toolkit</span>
          <h2>工具</h2>
        </div>
        <SubTabBar
          items={TOOLKIT_TABS}
          activeKey={activeTab}
          onChange={(key) => onNavigate(buildToolkitPath(key as ToolkitTabKey))}
        />
      </div>
      <ToolkitSection activeTab={activeTab} />
    </div>
  );
}
