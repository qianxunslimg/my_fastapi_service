/// <reference types="vite/client" />

type RuntimeEnvKey = "VITE_API_BASE";

type RuntimeEnv = Partial<Record<RuntimeEnvKey, string>>;

declare global {
  interface Window {
    __ENV__?: RuntimeEnv;
  }
}

export {};
