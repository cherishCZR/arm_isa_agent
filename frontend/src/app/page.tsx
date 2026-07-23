"use client";

import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Play, Layers, MessageSquare, BookOpen, ArrowRight } from "lucide-react";

const quickLinks = [
  {
    href: "/verify",
    icon: Play,
    title: "Verify Instruction",
    desc: "Run the full Compiler Verification pipeline for a single ARM A64 instruction.",
    action: "Start Verifying",
  },
  {
    href: "/batch",
    icon: Layers,
    title: "Batch Verification",
    desc: "Verify multiple instructions in sequence with real-time progress tracking.",
    action: "Batch Verify",
  },
  {
    href: "/chat",
    icon: MessageSquare,
    title: "Copilot Chat",
    desc: "Ask questions about ARM instructions and get AI-powered responses.",
    action: "Start Chat",
  },
  {
    href: "/explore",
    icon: BookOpen,
    title: "Explore Instructions",
    desc: "Browse the ARM A64 instruction set with encoding details and variants.",
    action: "Explore",
  },
];

export default function Home() {
  return (
    <div className="max-w-3xl mx-auto pt-12">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold mb-3">
          🧪 ARM ISA Compiler Verification
        </h1>
        <p className="text-muted-foreground text-lg max-w-lg mx-auto">
          AI-powered automated compiler verification agent for ARM A64 instruction set.
          Generate, review, and repair test cases in real-time.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {quickLinks.map((link) => (
          <Link key={link.href} href={link.href}>
            <Card className="h-full hover:border-primary/40 hover:shadow-sm transition-all cursor-pointer group">
              <CardHeader className="pb-2">
                <div className="flex items-center gap-2">
                  <link.icon className="w-5 h-5 text-primary" />
                  <CardTitle className="text-base">{link.title}</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="mb-3">{link.desc}</CardDescription>
                <span className="text-sm text-primary font-medium inline-flex items-center gap-1 group-hover:gap-2 transition-all">
                  {link.action} <ArrowRight className="w-3 h-3" />
                </span>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      <div className="mt-8 text-center">
        <p className="text-xs text-muted-foreground">
          Backed by ARM Architecture Reference Manual (DDI 0487) · 2000+ instructions
        </p>
      </div>
    </div>
  );
}
