import Link from "next/link";

export default function Navigation() {
    return (<div className="w-full h-16 bg-zinc-400 dark:bg-zinc-600 flex flex-row items-center justify-between p-4">
        <Link href="/" className="text-2xl font-bold text-zinc-700 dark:text-zinc-300">La Esquina AQP</Link>
    </div>)
}