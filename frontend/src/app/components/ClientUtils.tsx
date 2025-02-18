"use client";

export function isSettingEnabled(setting: string): boolean {
  const item = localStorage.getItem("settings-" + setting);
  if (item && item === "true")
    return true;
  return false;
}