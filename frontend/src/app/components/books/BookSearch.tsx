"use client";

import { useEffect, useState } from "react";
import { API_URL } from "../Constants";
import { Book, Category } from "../Models";
import { isSettingEnabled, prettyString } from "../../others/Utils";

function BookTableHeader({ text }: { text: string }) {
  return (
    <th className="text-zinc-700 dark:text-zinc-300 border-t border-b p-1 border-zinc-700 bg-zinc-400 dark:bg-zinc-600 dark:border-zinc-300">{text}</th>
  );
}

function BookTableRow({ children }: { children: React.ReactNode }) {
  return (
    <td className="text-zinc-700 dark:text-zinc-300 text-center border-t border-b p-1 border-zinc-700 dark:border-zinc-300">{children}</td>
  );
}

function BookSearchInput({ text, id }: { text: string, id: string }) {
  return (
    <>
      <p className="text-md font-bold text-zinc-700 dark:text-zinc-300">{text}</p>
      <input id={id} type="text" className="w-full bg-zinc-100 dark:bg-zinc-400 py-2 px-4 border border-zinc-400 dark:border-zinc-600 rounded-2xl" placeholder={text} />
    </>
  );
}

export default function BookSearch() {
  let [books, setBooks] = useState<Book[]>([]);
  let [categories, setCategories] = useState<Category[]>([]);
  let completeSearch = isSettingEnabled("complete-search");

  useEffect(() => {
    fetch(API_URL + "/categories")
      .then(response => response.json() as Promise<Category[]>)
      .then(data => setCategories(data));
  }, []);

  function deleteBook(id: number) {
    const confirmation = confirm("¿Estás seguro de que deseas eliminar este libro?");
    if (!confirmation) return;
    fetch(`${API_URL}/books/${id}`, { method: "DELETE" })
      .then(() => setBooks(books.filter(book => book.id !== id)));
  }

  function editBook(book: Book) {
    location.href = `/books/edit/?id=${book.id}&title=${book.title}&author=${book.author}&edition=${book.edition}&price=${book.price}&category=${book.category_id}`;
  }

  function downloadBook(id: number, name: string) {
    fetch(`${API_URL}/books/${id}/download`, { method: "GET" })
      .then(response => response.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = name + ".pdf";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      });
  }

  function doSearch() {
    const queryElem = document.getElementById("query") as HTMLInputElement;
    const query = queryElem.value;
    queryElem.value = "";
    const results = document.getElementById("results") as HTMLElement;
    if (query) {
      const formData = new FormData();
      formData.append("query", query.toLowerCase());
      fetch(API_URL + "/books/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams(formData as unknown as Record<string, string>)
      })
        .then(response => response.json() as Promise<Book[]>)
        .then(data => setBooks(data))
        .then(() => results.scrollIntoView({ behavior: "smooth" }));
    }
  }

  function doCompleteSearch() {
    const titleElem = document.getElementById("title") as HTMLInputElement;
    const title = titleElem.value;
    titleElem.value = "";
    const authorElem = document.getElementById("author") as HTMLInputElement;
    const author = authorElem.value;
    authorElem.value = "";
    const results = document.getElementById("results") as HTMLElement;
    const formData = new FormData();
    if (title || author) {
      if (title)
        formData.append("title", title.toLowerCase());
      if (author)
        formData.append("author", author.toLowerCase());
      console.log(formData);
      fetch(API_URL + "/books/complete-search", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams(formData as unknown as Record<string, string>)
      })
        .then(response => response.json() as Promise<Book[]>)
        .then(data => setBooks(data))
        .then(() => results.scrollIntoView({ behavior: "smooth" }));
    }
  }

  return (
    <div className="flex flex-col items-start gap-8 p-4 w-full">
      <div className="flex flex-col gap-1 w-full">
        {completeSearch ?
          <>
            <BookSearchInput text="Título" id="title" />
            <BookSearchInput text="Autor" id="author" />
            <span className="h-2"></span>
            <button className="px-4 py-2 w-36 bg-zinc-400 dark:bg-zinc-600 text-zinc-700 dark:text-zinc-300 rounded-2xl" onClick={doCompleteSearch}>Buscar</button>
          </> :
          <>
            <BookSearchInput text="Búsqueda" id="query" />
            <span className="h-2"></span>
            <button className="px-4 py-2 w-36 bg-zinc-400 dark:bg-zinc-600 text-zinc-700 dark:text-zinc-300 rounded-2xl" onClick={doSearch}>Buscar</button>
          </>}
      </div>
      <table className="w-full" id="results">
        <thead>
          <tr>
            <BookTableHeader text="ID" />
            <BookTableHeader text="Título" />
            <BookTableHeader text="Autor" />
            <BookTableHeader text="Edición" />
            <BookTableHeader text="Precio" />
            <BookTableHeader text="Categoría" />
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
              <BookTableRow>{prettyString(categories.find(c => c.id === book.category_id)!.name)}</BookTableRow>
              <BookTableRow>
                {isSettingEnabled("advanced") &&
                  <>
                    <button className="hover:font-bold px-1 text-zinc-700 dark:text-zinc-300" onClick={() => editBook(book)}>Editar</button>
                    <button className="hover:font-bold px-1 text-zinc-700 dark:text-zinc-300" onClick={() => deleteBook(book.id)}>Eliminar</button>
                  </>}
                <button onClick={() => downloadBook(book.id, prettyString(book.title))} className="hover:font-bold px-1 text-zinc-700 dark:text-zinc-300">Descargar</button>
              </BookTableRow>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}