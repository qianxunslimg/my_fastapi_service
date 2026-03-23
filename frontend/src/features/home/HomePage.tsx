import { OverviewGrid } from "./OverviewGrid";
import { HeroSection } from "./HeroSection";

type HomePageProps = {
  onNavigate: (path: string) => void;
};

export function HomePage({ onNavigate }: HomePageProps) {
  return (
    <div className="page-stack">
      <HeroSection />
      <OverviewGrid onNavigate={onNavigate} />
    </div>
  );
}
