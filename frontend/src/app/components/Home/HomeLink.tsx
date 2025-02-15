import { IconDefinition } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";

export default function HomeLink({ dest, icon, label }: { dest: string, icon: IconDefinition, label: string }) {
    return (
        <Link href={dest} className="flex justify-center flex-col items-center h-32 bg-zinc-400 dark:bg-zinc-600 text-zinc-700 dark:text-zinc-300 p-4">
            <FontAwesomeIcon icon={icon} className="text-zinc-700 dark:text-zinc-300" />
            <p className="text-2xl font-bold">{label}</p>
        </Link>
    );

}