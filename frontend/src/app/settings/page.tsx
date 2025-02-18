"use client";

function SettingsSwitch({ label, localName }: { label: string, localName: string }) {
  const internalID = `settings-switch-${localName}`;
  function setSetting() {
    const setting = document.getElementById(internalID) as HTMLInputElement;
    localStorage.setItem(localName, setting.checked.toString());
  }
  return (
    <div className="flex flex-row items-center gap-4">
      <div className="relative inline-block w-11 h-5">
        <input defaultChecked={false} id={internalID} type="checkbox" className="peer appearance-none w-11 h-5 bg-zinc-500 dark:bg-zinc-500 rounded-full cursor-pointer transition-colors duration-300" onChange={setSetting} />
        <label htmlFor={internalID} className="absolute top-0 left-0 w-5 h-5 bg-white rounded-full border border-zinc-300 shadow-sm transition-transform duration-300 peer-checked:translate-x-6 peer-checked:border-zinc-800 cursor-pointer">
        </label>
      </div>
      <p className="text-lg font-bold text-zinc-700 dark:text-zinc-300">{label}</p>
    </div>
  )
}

export default function Settings() {
  return (
    <div className="w-full h-full p-8">
      <p className="font-extrabold text-5xl text-zinc-700 dark:text-zinc-300 text-center">Configuración</p>
      <div className="flex flex-col gap-4 py-4">
        <SettingsSwitch label="Opciones avanzadas" localName="settings-advanced" />
      </div>
    </div>
  )
}