export interface OpenAppInfo {
  windowEl: HTMLDivElement;
  taskbarButton: HTMLDivElement;
}

export type GeminiOpenAppsMap = Map<string, OpenAppInfo>;

export interface DosInstance {
  initialized: boolean;
}

export type DosInstances = Record<string, DosInstance>;

export function createOpenAppsMap(): GeminiOpenAppsMap {
  return new Map<string, OpenAppInfo>();
}
