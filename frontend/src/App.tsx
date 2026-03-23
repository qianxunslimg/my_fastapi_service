import { ConfigProvider, theme } from "antd";
import { useEffect, useState } from "react";

import { SiteHeader } from "./layout/SiteHeader";
import { parseRoute } from "./app/routes";
import type { RouteState } from "./app/types";
import { HomePage } from "./features/home/HomePage";
import { ProjectsPage } from "./features/projects/ProjectsPage";
import { WritingPage } from "./features/writing/WritingPage";
import { ToolkitPage } from "./features/toolkit/ToolkitPage";

const antdTheme = {
  algorithm: theme.defaultAlgorithm,
  token: {
    colorPrimary: "#b55c38",
    colorInfo: "#b55c38",
    colorSuccess: "#2f6b59",
    colorWarning: "#bb7a2f",
    colorError: "#c5422d",
    colorBgBase: "#f3ede5",
    colorBgContainer: "#faf6ef",
    colorText: "#171411",
    colorTextSecondary: "#63584c",
    colorBorder: "rgba(47, 34, 24, 0.12)",
    borderRadius: 22,
    fontFamily: '"Avenir Next", "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Source Han Sans SC", sans-serif',
  },
};

export default function App() {
  const [route, setRoute] = useState<RouteState>(() => parseRoute(window.location.pathname));

  useEffect(() => {
    const syncRoute = () => {
      const nextRoute = parseRoute(window.location.pathname);
      if (window.location.pathname !== nextRoute.canonicalPath) {
        window.history.replaceState({}, "", nextRoute.canonicalPath);
        setRoute({
          ...nextRoute,
          path: nextRoute.canonicalPath,
        });
        return;
      }
      setRoute(nextRoute);
    };

    syncRoute();
    window.addEventListener("popstate", syncRoute);
    return () => window.removeEventListener("popstate", syncRoute);
  }, []);

  useEffect(() => {
    const titleMap = {
      home: "My FastAPI Service",
      projects: "项目 | My FastAPI Service",
      writing: "写作 | My FastAPI Service",
      toolkit: route.toolkitTab === "health" ? "服务状态 | My FastAPI Service" : "班易评 | My FastAPI Service",
    };

    document.title = titleMap[route.page];
  }, [route.page, route.toolkitTab]);

  function handleNavigate(path: string) {
    const nextRoute = parseRoute(path);
    const targetPath = nextRoute.canonicalPath;

    if (window.location.pathname === targetPath) {
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }

    window.history.pushState({}, "", targetPath);
    setRoute({
      ...nextRoute,
      path: targetPath,
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  let pageContent;

  switch (route.page) {
    case "projects":
      pageContent = <ProjectsPage />;
      break;
    case "writing":
      pageContent = <WritingPage />;
      break;
    case "toolkit":
      pageContent = <ToolkitPage activeTab={route.toolkitTab} onNavigate={handleNavigate} />;
      break;
    case "home":
    default:
      pageContent = <HomePage onNavigate={handleNavigate} />;
      break;
  }

  return (
    <ConfigProvider theme={antdTheme}>
      <div className="site-shell">
        <div className="background-orb background-orb-left" />
        <div className="background-orb background-orb-right" />
        <SiteHeader activePage={route.page} onNavigate={handleNavigate} />
        <main className="site-main">
          {pageContent}
        </main>
      </div>
    </ConfigProvider>
  );
}
