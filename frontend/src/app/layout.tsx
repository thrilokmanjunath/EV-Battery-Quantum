import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EV Battery Quantum Optimization",
  description: "Quantum Optimization Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`min-h-screen bg-quantum-dark text-white`}>{children}</body>
    </html>
  );
}
