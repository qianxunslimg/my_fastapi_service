import type { OpsTabKey, PageKey, RouteState, ToolkitTabKey } from "./types";

function normalizePath(pathname: string) {
  const trimmed = pathname.replace(/\/+$/, "");
  return trimmed || "/";
}

export function buildToolkitPath(tab: ToolkitTabKey) {
  return "/toolkit/" + tab;
}

export function buildOpsPath(tab: OpsTabKey) {
  return "/ops/" + tab;
}

export function buildPagePath(page: PageKey) {
  switch (page) {
    case "home":
      return "/";
    case "toolkit":
      return buildToolkitPath("banyiping");
    case "ops":
      return buildOpsPath("features");
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
        opsTab: "features",
        path,
        canonicalPath: "/",
      };
    case "/toolkit":
      return {
        page: "toolkit",
        toolkitTab: "banyiping",
        opsTab: "features",
        path,
        canonicalPath: buildToolkitPath("banyiping"),
      };
    case "/toolkit/banyiping":
      return {
        page: "toolkit",
        toolkitTab: "banyiping",
        opsTab: "features",
        path,
        canonicalPath: buildToolkitPath("banyiping"),
      };
    case "/toolkit/health":
      return {
        page: "ops",
        toolkitTab: "banyiping",
        opsTab: "features",
        path,
        canonicalPath: buildOpsPath("features"),
      };
    case "/toolkit/intake":
      return {
        page: "toolkit",
        toolkitTab: "banyiping",
        opsTab: "features",
        path,
        canonicalPath: buildToolkitPath("banyiping"),
      };
    case "/ops":
      return {
        page: "ops",
        toolkitTab: "banyiping",
        opsTab: "features",
        path,
        canonicalPath: buildOpsPath("features"),
      };
    case "/ops/features":
      return {
        page: "ops",
        toolkitTab: "banyiping",
        opsTab: "features",
        path,
        canonicalPath: buildOpsPath("features"),
      };
    case "/ops/logs":
      return {
        page: "ops",
        toolkitTab: "banyiping",
        opsTab: "logs",
        path,
        canonicalPath: buildOpsPath("logs"),
      };
    case "/ops/table":
      return {
        page: "ops",
        toolkitTab: "banyiping",
        opsTab: "table",
        path,
        canonicalPath: buildOpsPath("table"),
      };
    default:
      return {
        page: "home",
        toolkitTab: "banyiping",
        opsTab: "features",
        path,
        canonicalPath: "/",
      };
  }
}
