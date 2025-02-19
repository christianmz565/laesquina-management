"use client";

import BackButton from "@/app/components/BackButton";
import { useState } from "react";

function BookInput({ innerID }: { innerID: number }) {
  const inputStyle = "px-4 py-2 w-full bg-zinc-400 dark:bg-zinc-600 text-zinc-700 dark:text-zinc-300 placeholder-zinc-700 dark:placeholder-zinc-300 border border-zinc-300 dark:border-zinc-700";

  return (
    <div className="grid grid-cols-2 gap-1">
      <input type="text" placeholder="Título" id={innerID + "-title"} className={inputStyle} />
      <input type="text" placeholder="Autor" id={innerID + "-author"} className={inputStyle} />
      <input type="text" placeholder="Edición" id={innerID + "-edition"} className={inputStyle} />
      <input type="text" placeholder="Precio" id={innerID + "-price"} className={inputStyle} />
      <input type="file" accept=".pdf" id={innerID + "-file"} className={inputStyle} />
    </div>
  )
}

export default function BooksCreate() {
  let [currentID, setCurrentID] = useState(1);
  let [bookInputs, setBookInputs] = useState([<BookInput innerID={0} />]);

  function addBookInput() {
    setCurrentID(currentID + 1);
    setBookInputs([...bookInputs, <BookInput innerID={currentID} />]);
  }

  function createBooks() {
    let books = [];
    for (let i = 0; i < currentID; i++) {
      let title = document.getElementById(i + "-title") as HTMLInputElement;
      let author = document.getElementById(i + "-author") as HTMLInputElement;
      let edition = document.getElementById(i + "-edition") as HTMLInputElement;
      let price = document.getElementById(i + "-price") as HTMLInputElement;
      let file = document.getElementById(i + "-file") as HTMLInputElement;

      if (title.value && author.value && edition.value && price.value && file.files) {
        let formData = new FormData();
        formData.append("title", title.value);
        formData.append("author", author.value);
        formData.append("edition", edition.value);
        formData.append("price", price.value);
        formData.append("file", file.files[0]);

        books.push(formData);
      }
    }
    console.log(books);
  }
  return (
    <div className="w-full h-full p-8 relative">
      <BackButton />
      <p className="font-extrabold text-4xl text-zinc-700 dark:text-zinc-300 text-center">Crear libro(s)</p>
      <div className="flex flex-col gap-4 py-4 w-full">
        {bookInputs.map((input, index) => (
          <div key={index}>
            {input}
          </div>
        ))}
      </div>
      <div className="flex flex-row w-full gap-4 justify-center">
        <button className="px-4 py-2 w-36 bg-zinc-400 dark:bg-zinc-600 text-zinc-700 dark:text-zinc-300 rounded-2xl" onClick={addBookInput}>Añadir</button>
        <button className="px-4 py-2 w-36 bg-zinc-400 dark:bg-zinc-600 text-zinc-700 dark:text-zinc-300 rounded-2xl" onClick={createBooks}>Crear</button>
      </div>
    </div>
  )
}