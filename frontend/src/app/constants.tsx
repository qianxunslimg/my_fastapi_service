import {
  ExperimentOutlined,
  HighlightOutlined,
  HomeOutlined,
  ProfileOutlined,
} from "@ant-design/icons";
import { buildPagePath } from "./routes";
import type { NavItem, ToolkitTabItem } from "./types";

export const SITE_NAME = "My FastAPI Service";
export const SITE_SUBTITLE = "Projects, writing, and API tools";

export const NAV_ITEMS: NavItem[] = [
  { key: "home", label: "首页", icon: <HomeOutlined />, path: buildPagePath("home") },
  { key: "projects", label: "项目", icon: <ProfileOutlined />, path: buildPagePath("projects") },
  { key: "writing", label: "写作", icon: <HighlightOutlined />, path: buildPagePath("writing") },
  { key: "toolkit", label: "工具", icon: <ExperimentOutlined />, path: buildPagePath("toolkit") },
];

export const TOOLKIT_TABS: ToolkitTabItem[] = [
  { key: "banyiping", label: "班易评" },
  { key: "health", label: "服务状态" },
];

export const FEATURE_PILLS = [
  "FastAPI",
  "React",
  "Docker",
  "Toolkit",
];

export const HERO_NOTES = [
  {
    label: "Structure",
    title: "backend / frontend / db",
    description: "拆分清楚，后面继续加功能不会乱。",
  },
  {
    label: "Stack",
    title: "FastAPI + React",
    description: "前后端同仓库，工具页直接接接口。",
  },
  {
    label: "Mode",
    title: "Portfolio + toolkit",
    description: "展示和真实可用的功能放在一起。",
  },
];

export const OVERVIEW_ITEMS = [
  {
    label: "Projects",
    title: "项目",
    description: "把做过的东西整理成作品集。",
  },
  {
    label: "Writing",
    title: "写作",
    description: "记录方法、判断和过程。",
  },
  {
    label: "Toolkit",
    title: "工具",
    description: "页面里直接接住后端能力。",
  },
];

export const PROJECTS = [
  {
    title: "Personal Website Platform",
    category: "Core",
    description: "个人站骨架，承接展示、写作和工具。",
    meta: "FastAPI / React / Docker",
  },
  {
    title: "BYP Analyze Tool",
    category: "Utility",
    description: "班易评分析工具，前端输入 URL，后端返回统计结果。",
    meta: "Pandas / Requests / API Integration",
  },
  {
    title: "Reusable Site Skeleton",
    category: "Foundation",
    description: "参考成熟项目的边界划分，做成可持续复用的模板。",
    meta: "Config / Layout / Feature Modules",
  },
];

export const WRITING_ITEMS = [
  {
    category: "System",
    title: "为什么个人网站也值得做前后端分层",
    summary: "结构先立住，后面内容才接得稳。",
    meta: "边界先于样式",
  },
  {
    category: "Product",
    title: "把工具页纳入个人站，而不是另起一个后台",
    summary: "展示和实用能力不必分家。",
    meta: "站点也能是工具入口",
  },
  {
    category: "Taste",
    title: "从业务平台借结构，而不是复制业务复杂度",
    summary: "借的是方法，不是后台味道。",
    meta: "克制比堆功能更重要",
  },
];
