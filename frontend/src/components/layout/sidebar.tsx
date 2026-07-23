"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  Play,
  Layers,
  MessageSquare,
  BookOpen,
  History,
  Settings,
  Menu,
  X,
  Home,
} from "lucide-react";
import { Button } from "@/components/ui/button";

const navItems = [
  { href: "/", label: "Home", icon: Home },
  { href: "/verify", label: "Verify", icon: Play },
  { href: "/batch", label: "Batch", icon: Layers },
  { href: "/chat", label: "Chat", icon: MessageSquare },
  { href: "/explore", label: "Explore", icon: BookOpen },
  { href: "/history", label: "History", icon: History },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  const closeMobile = () => setMobileOpen(false);

  return (
    <>
      {/* Mobile hamburger */}
      <button
        className="fixed top-3 left-3 z-50 md:hidden p-2 rounded-md bg-background border shadow-sm"
        onClick={() => setMobileOpen(!mobileOpen)}
        aria-label="Toggle menu"
      >
        {mobileOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
      </button>

      {/* Overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-40 md:hidden"
          onClick={closeMobile}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed md:sticky top-0 left-0 z-50 md:z-auto h-full w-64 md:w-16 lg:w-56 border-r bg-card flex flex-col shrink-0 transition-transform",
          "md:translate-x-0",
          mobileOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="h-14 flex items-center gap-2 px-4 border-b shrink-0">
          <span className="text-lg">🧪</span>
          <span className="font-semibold text-sm hidden lg:block">
            ARM ISA Agent
          </span>
        </div>

        <nav className="flex-1 p-2 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const active =
              pathname === item.href ||
              (item.href !== "/" && pathname.startsWith(item.href));
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={closeMobile}
                className={cn(
                  "flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors",
                  active
                    ? "bg-primary/10 text-primary font-medium"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground",
                )}
              >
                <item.icon className="w-4 h-4 shrink-0" />
                <span className="lg:hidden xl:block truncate">{item.label}</span>
                <span className="hidden lg:block xl:hidden truncate">{item.label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="p-3 border-t text-xs text-muted-foreground hidden lg:block shrink-0">
          v0.1.0
        </div>
      </aside>
    </>
  );
}
