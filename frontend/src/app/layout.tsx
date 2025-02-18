import type { Metadata } from "next";
import { Work_Sans } from "next/font/google";
import "./globals.css";
import Navigation from "./components/Navigation";

const geistSans = Work_Sans({
  variable: "--font-work-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "La Esquina AQP",
  description: ".",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} antialiased w-screen bg-zinc-300 dark:bg-zinc-700`}
      >
        <Navigation />
        {children}
      </body>
    </html>
  );
}
