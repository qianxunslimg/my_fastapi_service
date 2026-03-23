import { Button } from "antd";

import { NAV_ITEMS, SITE_NAME, SITE_SUBTITLE } from "../app/constants";
import { env } from "../env";
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
        <span className="site-brand-mark">MF</span>
        <span className="site-brand-copy">
          <strong>{SITE_NAME}</strong>
          <small>{SITE_SUBTITLE}</small>
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

      <div className="site-header-actions">
        <Button size="large" className="ghost-action" href={`${env.apiBase}/docs`} target="_blank">
          API Docs
        </Button>
      </div>
    </header>
  );
}
