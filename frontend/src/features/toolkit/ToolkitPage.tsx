import type { ToolkitTabKey } from "../../app/types";
import { ToolkitSection } from "./ToolkitSection";

type ToolkitPageProps = {
  activeTab: ToolkitTabKey;
};

export function ToolkitPage({ activeTab }: ToolkitPageProps) {
  return (
    <div className="page-stack">
      <ToolkitSection activeTab={activeTab} />
    </div>
  );
}
