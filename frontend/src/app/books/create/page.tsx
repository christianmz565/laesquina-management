"use client";

import BackButton from "@/app/components/BackButton";
import { API_URL } from "@/app/components/Constants";
import { Category } from "@/app/components/Models";
import { prettyString } from "@/app/others/Utils";
import { useEffect, useState } from "react";

function BookInput({ innerID, onRemove, categories }: { innerID: number, onRemove: (id: number) => void, categories: Category[] }) {
  const inputStyle = "px-4 py-2 w-full bg-zinc-400 dark:bg-zinc-600 text-zinc-700 dark:text-zinc-300 placeholder-zinc-700 dark:placeholder-zinc-300 border border-zinc-300 dark:border-zinc-700";

  return (
    <div className="grid grid-cols-2 gap-1">
      <input type="text" placeholder="Título" id={innerID + "-title"} className={inputStyle} />
      <input type="text" placeholder="Autor" id={innerID + "-author"} className={inputStyle} />
      <input type="text" placeholder="Edición" id={innerID + "-edition"} className={inputStyle} />
      <input type="text" placeholder="Precio" id={innerID + "-price"} className={inputStyle} />
      <input type="file" accept=".pdf" id={innerID + "-file"} className={inputStyle} />
      <select id={innerID + "-category"} className={inputStyle}>
        {categories.map((category) => (
          <option key={category.id} value={category.id}>{prettyString(category.name)}</option>
        ))}
      </select>
      <button className="px-4 py-2 w-full bg-red-400 dark:bg-red-500 text-zinc-700 dark:text-zinc-300" onClick={() => onRemove(innerID)}>Eliminar</button>
    </div>
  )
}

export default function BooksCreate() {
  let [currentID, setCurrentID] = useState(1);
  let [bookInputs, setBookInputs] = useState<number[]>([0]);
  let [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    fetch(API_URL + "/categories")
      .then(response => response.json() as Promise<Category[]>)
      .then(data => setCategories(data));
  }, []);

  function handleRemove(id: number) {
    let newInputs = bookInputs.filter((input) => input !== id);
    setBookInputs(newInputs);
  }

  function addBookInput() {
    setCurrentID(currentID + 1);
    setBookInputs([...bookInputs, currentID]);
  }

  async function createBooks() {
    for (let i of bookInputs) {
      let title = document.getElementById(i + "-title") as HTMLInputElement;
      let author = document.getElementById(i + "-author") as HTMLInputElement;
      let edition = document.getElementById(i + "-edition") as HTMLInputElement;
      let price = document.getElementById(i + "-price") as HTMLInputElement;
      let file = document.getElementById(i + "-file") as HTMLInputElement;
      let category = document.getElementById(i + "-category") as HTMLSelectElement;

      if (title.value && author.value && edition.value && price.value && file.files && category.value) {
        let formData = new FormData();
        formData.append("title", title.value);
        formData.append("author", author.value);
        formData.append("edition", edition.value);
        formData.append("price", price.value);
        formData.append("category_id", category.value);
        formData.append("file", file.files[0]);

        const response = await fetch(API_URL + "/books/create", {
          method: "POST",
          body: formData
        });
        const book = await response.json();
        console.log(book);
      }
    }
    setBookInputs([]);
    addBookInput();
  }
  return (
    <div className="w-full h-full p-8 relative">
      <BackButton />
      <p className="font-extrabold text-4xl text-zinc-700 dark:text-zinc-300 text-center">Crear libro(s)</p>
      <div className="flex flex-col gap-4 py-4 w-full">
        {bookInputs.map((input) => (
          <BookInput key={input} innerID={input} onRemove={handleRemove} categories={categories} />
        ))
        }
      </div>
      <div className="flex flex-row w-full gap-4 justify-center">
        <button className="px-4 py-2 w-36 bg-zinc-400 dark:bg-zinc-600 text-zinc-700 dark:text-zinc-300 rounded-2xl" onClick={addBookInput}>Añadir</button>
        <button className="px-4 py-2 w-36 bg-zinc-400 dark:bg-zinc-600 text-zinc-700 dark:text-zinc-300 rounded-2xl" onClick={createBooks}>Crear</button>
      </div>
    </div>
  )
}