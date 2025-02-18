import { faBook } from "@fortawesome/free-solid-svg-icons";
import HomeLink from "./components/Home/HomeLink";

export default function Home() {

  return (
    <div className="w-full h-full p-8">
      <p className="font-extrabold text-6xl text-zinc-700 dark:text-zinc-300 text-center">La Esquina</p>
      <div className="grid grid-cols-1 gap-4 p-8">
        <HomeLink dest="/books" icon={faBook} label="Libros" />
      </div>
    </div>
  );
}
