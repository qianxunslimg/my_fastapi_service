import { OverviewGrid } from "./OverviewGrid";

type HomePageProps = {
  onNavigate: (path: string) => void;
};

export function HomePage({ onNavigate }: HomePageProps) {
  return (
    <div className="page-stack">
      <OverviewGrid onNavigate={onNavigate} />
    </div>
  );
}
