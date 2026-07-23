import type { Metadata } from "next";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Sidebar } from "@/components/layout/sidebar";
import "./globals.css";

export const metadata: Metadata = {
  title: "ARM ISA Verification Agent",
  description: "AI-powered Compiler Verification Agent for ARM A64 instruction set",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col md:flex-row">
        <TooltipProvider>
          <Sidebar />
          {/* Spacer for mobile hamburger button */}
          <div className="h-10 md:hidden shrink-0" />
          <main className="flex-1 overflow-auto p-4 sm:p-6 md:pt-6">
            {children}
          </main>
        </TooltipProvider>
      </body>
    </html>
  );
}
