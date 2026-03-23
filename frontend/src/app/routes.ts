import type { PageKey, RouteState, ToolkitTabKey } from "./types";

function normalizePath(pathname: string) {
  const trimmed = pathname.replace(/\/+$/, "");
  return trimmed || "/";
}

export function buildToolkitPath(tab: ToolkitTabKey) {
  return `/toolkit/${tab}`;
}

export function buildPagePath(page: PageKey) {
  switch (page) {
    case "home":
      return "/";
    case "projects":
      return "/projects";
    case "writing":
      return "/writing";
    case "toolkit":
      return buildToolkitPath("banyiping");
    default:
      return "/";
  }
}

export function parseRoute(pathname: string): RouteState {
  const path = normalizePath(pathname);

  switch (path) {
    case "/":
      return {
        page: "home",
        toolkitTab: "banyiping",
        path,
        canonicalPath: "/",
      };
    case "/projects":
      return {
        page: "projects",
        toolkitTab: "banyiping",
        path,
        canonicalPath: "/projects",
      };
    case "/writing":
      return {
        page: "writing",
        toolkitTab: "banyiping",
        path,
        canonicalPath: "/writing",
      };
    case "/toolkit":
    case "/toolkit/banyiping":
      return {
        page: "toolkit",
        toolkitTab: "banyiping",
        path,
        canonicalPath: buildToolkitPath("banyiping"),
      };
    case "/toolkit/health":
      return {
        page: "toolkit",
        toolkitTab: "health",
        path,
        canonicalPath: buildToolkitPath("health"),
      };
    default:
      return {
        page: "home",
        toolkitTab: "banyiping",
        path,
        canonicalPath: "/",
      };
  }
}
