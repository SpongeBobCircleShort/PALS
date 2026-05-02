import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Physics Pals",
  description: "A Socratic physics tutor powered by textbook retrieval."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
