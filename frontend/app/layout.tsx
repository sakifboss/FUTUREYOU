import type { Metadata } from "next";
import { Inter } from "next/font/google";

import { Nav } from "@/components/layout/nav";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "FutureYou",
  description: "AI-powered decision intelligence and scenario simulation.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen bg-paper text-ink antialiased dark:bg-midnight dark:text-paper`}>
        <Nav />
        {children}
      </body>
    </html>
  );
}
