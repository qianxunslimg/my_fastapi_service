import type { ReactNode } from "react";

export type PageKey = "home" | "projects" | "writing" | "toolkit";
export type ToolkitTabKey = "banyiping" | "health";

export type NavItem = {
  key: PageKey;
  label: string;
  icon: ReactNode;
  path: string;
};

export type ToolkitTabItem = {
  key: ToolkitTabKey;
  label: string;
};

export type RouteState = {
  page: PageKey;
  toolkitTab: ToolkitTabKey;
  path: string;
  canonicalPath: string;
};
