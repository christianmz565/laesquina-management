"use client";

import { useState } from "react";
import { API_URL } from "../Constants";
import { Book } from "../Models";

export function BookTableHeader({ text }: { text: string }) {
  return (
    <th className="text-zinc-700 dark:text-zinc-300 border border-zinc-700 bg-zinc-400 dark:bg-zinc-600 dark:border-zinc-300">{text}</th>
  );
}

export function BookTableRow({ children }: { children: React.ReactNode }) {
  return (
    <td className="text-zinc-700 dark:text-zinc-300 text-center border border-zinc-700 dark:border-zinc-300">{children}</td>
  );
}


export default function BookSearch() {
  let [books, setBooks] = useState<Book[]>([]);

  function prettyString(str: string) {
    let result = "";
    str.split("-").forEach(word => {
      if (word.length > 4)
        result += word.charAt(0).toUpperCase() + word.slice(1) + " ";
      else
        result += word + " ";
    });
    return result;
  }

  async function doSearch() {
    const title = (document.getElementById("title") as HTMLInputElement).value;
    const author = (document.getElementById("author") as HTMLInputElement).value;
    const formData = new FormData();
    if (title || author) {
      if (title)
        formData.append("title", title);
      if (author)
        formData.append("author", author);
      console.log(formData);
      const books = await fetch(API_URL + "/books/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams(formData as unknown as Record<string, string>)
      });

      const searchResponse = await books.json() as Book[];
      setBooks(searchResponse);
    }
  }

  return (
    <div className="flex flex-col items-center gap-1 p-4 w-full">
      <p className="text-md font-bold text-zinc-700 dark:text-zinc-300">Título</p>
      <input id="title" type="text" className="w-3/4 bg-zinc-100 dark:bg-zinc-400 py-2 px-4 border border-zinc-400 dark:border-zinc-600 rounded-2xl" placeholder="Título" />
      <span></span>
      <p className="text-md font-bold text-zinc-700 dark:text-zinc-300">Autor</p>
      <input id="author" type="text" className="w-3/4 bg-zinc-100 dark:bg-zinc-400 py-2 px-4 border border-zinc-400 dark:border-zinc-600 rounded-2xl" placeholder="Autor" />
      <span className="h-2"></span>
      <button className="px-4 py-2 w-36 bg-zinc-400 dark:bg-zinc-600 text-zinc-700 dark:text-zinc-300 rounded-2xl" onClick={doSearch}>Buscar</button>
      <span className="h-8"></span>
      <table className="w-full">
        <thead>
          <tr>
            <BookTableHeader text="ID" />
            <BookTableHeader text="Título" />
            <BookTableHeader text="Autor" />
            <BookTableHeader text="Edición" />
            <BookTableHeader text="Precio" />
            <BookTableHeader text="Acciones" />
          </tr>
        </thead>
        <tbody>
          {books.map(book => (
            <tr key={book.id}>
              <BookTableRow>{book.id}</BookTableRow>
              <BookTableRow>{prettyString(book.title)}</BookTableRow>
              <BookTableRow>{prettyString(book.author)}</BookTableRow>
              <BookTableRow>{book.edition}</BookTableRow>
              <BookTableRow>S/.{book.price}</BookTableRow>
              <BookTableRow>
                <button className="p-2 hover:font-bold text-zinc-700 w-20 dark:text-zinc-300">Editar</button>
                <button className="p-2 hover:font-bold text-zinc-700 w-20 dark:text-zinc-300">Eliminar</button>
              </BookTableRow>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}