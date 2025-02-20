"use client";

import BackButton from "@/app/components/BackButton";
import { API_URL } from "@/app/components/Constants";
import { Category } from "@/app/components/Models";
import { prettyString } from "@/app/others/Utils";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

function BookEditInput({ name, children }: { name: string, children: React.ReactNode }) {
  return (
    <div className="flex flex-row w-full gap-4 items-center">
      <p className="font-bold text-zinc-700 w-24 dark:text-zinc-300">{name}</p>
      {children}
    </div>
  )
}

export default function BookEdit() {
  let [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    fetch(API_URL + "/categories")
      .then(response => response.json() as Promise<Category[]>)
      .then(data => setCategories(data));
  }, []);

  const searchParams = useSearchParams();
  const id = searchParams.get("id")!;
  const title = searchParams.get("title")!;
  const author = searchParams.get("author")!;
  const edition = searchParams.get("edition")!;
  const price = searchParams.get("price")!;
  const category_id = searchParams.get("category")!;

  const inputStyle = "px-4 py-2 w-full bg-zinc-100 dark:bg-zinc-900 text-zinc-800 dark:text-zinc-200 placeholder-zinc-800 dark:placeholder-zinc-200 border";

  function editBook() {
    const title = (document.getElementById("title") as HTMLInputElement).value;
    const author = (document.getElementById("author") as HTMLInputElement).value;
    const edition = (document.getElementById("edition") as HTMLInputElement).value;
    const price = (document.getElementById("price") as HTMLInputElement).value;
    const category = (document.getElementById("category") as HTMLSelectElement).value;
    const file = (document.getElementById("file") as HTMLInputElement).files?.[0];
    const formData = new FormData();
    formData.append("title", title);
    formData.append("author", author);
    formData.append("edition", edition);
    formData.append("price", price);
    formData.append("category_id", category);
    if (file) formData.append("file", file);
    fetch(`${API_URL}/books/${id}`, { method: "PUT", body: formData })
      .then(response => response.json())
      .then(data => console.log(data))
      .then(() => location.href = "/books");
  }

  return (
    <div className="w-full h-full p-8 relative">
      <BackButton />
      <p className="font-extrabold text-4xl text-zinc-700 dark:text-zinc-300 text-center">Editar libro</p>
      <div className="flex flex-col gap-4 py-4 w-full">
        <BookEditInput name="ID">
          <input type="text" placeholder="ID" defaultValue={id} className={inputStyle} readOnly />
        </BookEditInput>
        <BookEditInput name="Título">
          <input type="text" id="title" placeholder="Título" defaultValue={prettyString(title)} className={inputStyle} />
        </BookEditInput>
        <BookEditInput name="Autor">
          <input type="text" id="author" placeholder="Autor" defaultValue={prettyString(author)} className={inputStyle} />
        </BookEditInput>
        <BookEditInput name="Edición">
          <input type="text" id="edition" placeholder="Edición" defaultValue={edition} className={inputStyle} />
        </BookEditInput>
        <BookEditInput name="Precio">
          <input type="number" id="price" placeholder="Precio" defaultValue={price} className={inputStyle} />
        </BookEditInput>
        <BookEditInput name="Categoría">
          <select id="category" defaultValue={categories.find(category => category.id === parseInt(category_id))?.id} className={inputStyle}>
            {categories.map(category => (
              <option key={category.id} value={category.id}>{prettyString(category.name)}</option>
            ))}
          </select>
        </BookEditInput>
        <BookEditInput name="Archivo">
          <input type="file" id="file" className={inputStyle} />
        </BookEditInput>
        <button className="px-4 py-2 w-36 bg-zinc-400 dark:bg-zinc-600 text-zinc-700 dark:text-zinc-300 block m-auto" onClick={editBook}>Editar</button>
      </div>
    </div>
  )
}