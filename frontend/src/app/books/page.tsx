import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import BookSearch from "../components/books/BookSearch";

export default function Books() {
  return (
    <div className="w-full h-full p-8 relative">
      <Link href="/books/create" className="flex flex-row gap-1 text-zinc-700 dark:text-zinc-300 p-4 absolute top-2 right-2">
        <FontAwesomeIcon icon={faPlus} className="text-zinc-700 dark:text-zinc-300 w-12" />
      </Link>
      <p className="font-extrabold text-6xl text-zinc-700 dark:text-zinc-300 text-center">Libros</p>
      <BookSearch />
    </div>
  )
}