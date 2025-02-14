"use client";

import { useEffect, useState } from "react";

interface TextResponse {
  text: string;
};

interface FileResponse {
  filename: string;
};

export default function Home() {
  let [text, setText] = useState("");
  let [filename, setFilename] = useState("");

  useEffect(() => {
    send_text();
  }, []);

  async function send_text() {
    let text_response = await fetch("http://127.0.0.1:8000/get_text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: "test" }),
    });
    let text_data: TextResponse = await text_response.json();
    setText(text_data.text);
  }

  async function send_file() {
    let file_input = document.getElementById("file_input") as HTMLInputElement;
    let file = file_input.files![0];
    let file_form_data = new FormData();
    file_form_data.append("file", file);
    let file_response = await fetch("http://localhost:8000/upload_file", {
      method: "POST",
      body: file_form_data,
    });
    let file_data: FileResponse = await file_response.json();
    setFilename(file_data.filename);
  }

  return (
    <div>
      <p className="text-white">{text}</p>
      <form>
        <input type="file" id="file_input" />
        <button type="button" onClick={send_file}>
          Send File
        </button>
        <p className="text-white">{filename}</p>
      </form>
    </div>
  );
}
