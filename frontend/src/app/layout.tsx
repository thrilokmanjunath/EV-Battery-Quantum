import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EV Battery Quantum Optimization",
  description: "Quantum Optimization Dashboard",
};

import Navbar from "@/components/layout/Navbar";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`min-h-screen bg-zinc-50 text-zinc-900`}>
        <Navbar />
        {children}
      </body>
    </html>
  );
}
