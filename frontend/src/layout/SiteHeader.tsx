import { NAV_ITEMS, SITE_NAME } from "../app/constants";
import { buildPagePath } from "../app/routes";
import type { PageKey } from "../app/types";

type SiteHeaderProps = {
  activePage: PageKey;
  onNavigate: (path: string) => void;
};

export function SiteHeader({ activePage, onNavigate }: SiteHeaderProps) {
  return (
    <header className="site-header">
      <a
        href={buildPagePath("home")}
        className="site-brand"
        onClick={(event) => {
          event.preventDefault();
          onNavigate(buildPagePath("home"));
        }}
      >
        <span className="site-brand-mark">QX</span>
        <span className="site-brand-copy">
          <strong>{SITE_NAME}</strong>
        </span>
      </a>

      <nav className="site-nav" aria-label="主导航">
        {NAV_ITEMS.map((item) => (
          <a
            key={item.key}
            href={item.path}
            className={activePage === item.key ? "site-nav-item active" : "site-nav-item"}
            onClick={(event) => {
              event.preventDefault();
              onNavigate(item.path);
            }}
          >
            <span className="site-nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </a>
        ))}
      </nav>
    </header>
  );
}
