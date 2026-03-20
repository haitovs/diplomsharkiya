import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Toaster } from "react-hot-toast";

const inter = Inter({ subsets: ["latin", "cyrillic"] });

export const metadata: Metadata = {
  title: "Event Discovery — Turkmenistan",
  description: "Discover local events across Turkmenistan",
  icons: { icon: "/favicon.ico" },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tk">
      <body className={`${inter.className} bg-bg-primary text-text-primary min-h-screen`}>
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: "#FFFFFF",
              color: "#0F172A",
              border: "1px solid #E2E8F0",
              boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
            },
          }}
        />
        <Navbar />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
