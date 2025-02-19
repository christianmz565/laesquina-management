export function isSettingEnabled(setting: string): boolean {
  let enabled = false;
  if (typeof window !== "undefined") {
    const item = localStorage.getItem("settings-" + setting);
    if (item && item === "true")
      enabled = true;
  }
  return enabled;
}

export function prettyString(str: string) {
  let result = "";
  str.split("-").forEach(word => {
    if (word.length > 4)
      result += word.charAt(0).toUpperCase() + word.slice(1) + " ";
    else
      result += word + " ";
  });
  return result;
}