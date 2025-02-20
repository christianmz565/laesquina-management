"use client";

import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useEffect, useState } from "react";

export default function BackButton() {
  let [dest, setDest] = useState<string>("/");
  useEffect(() => {
    const curr = location.pathname;
    setDest(curr.substring(0, curr.lastIndexOf("/")) || "/");
  }, []);
  return (
    <div>
      <a href={dest} className="text-zinc-700 dark:text-zinc-300 p-4 absolute top-2 left-2">
        <FontAwesomeIcon icon={faArrowLeft} size="2x" className="text-zinc-700 dark:text-zinc-300 w-12" />
      </a>
    </div>
  )
}