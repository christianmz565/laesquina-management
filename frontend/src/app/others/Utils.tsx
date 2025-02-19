import { useEffect } from "react";

export function isSettingEnabled(setting: string): boolean {
  let enabled = false;
  if (typeof window !== "undefined") {
    const item = localStorage.getItem("settings-" + setting);
    if (item && item === "true")
      enabled = true;
  }
  return enabled;
}