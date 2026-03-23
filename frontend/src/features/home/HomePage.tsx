import { buildPagePath, buildToolkitPath } from "../../app/routes";
import { HeroSection } from "./HeroSection";
import { OverviewGrid } from "./OverviewGrid";

type HomePageProps = {
  onNavigate: (path: string) => void;
};

export function HomePage({ onNavigate }: HomePageProps) {
  return (
    <div className="page-stack">
      <HeroSection
        onJumpToTool={() => onNavigate(buildToolkitPath("banyiping"))}
        onJumpToProjects={() => onNavigate(buildPagePath("projects"))}
      />
      <OverviewGrid />
    </div>
  );
}
