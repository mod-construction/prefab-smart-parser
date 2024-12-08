import type { Metadata } from "next";
import { Header } from "./Header";
import "./globals.css";


export const metadata: Metadata = {
  title: "Parser",
  description: "Parse PDF and match it to BIM",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
    <body>
      <Header />
      <main className="bg-muted/50 flex h-100vh flex-1 flex-col">
        {children}
      </main>
    </body>
  </html>
  );
}
