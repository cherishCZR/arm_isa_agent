"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { Copy, Check } from "lucide-react";

interface CopyButtonProps {
  content: string;
  label?: string;
}

export function CopyButton({ content, label = "Copy" }: CopyButtonProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    const text = String(content ?? "");
    if (!text) return;

    const fallbackCopy = () => {
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.style.position = "fixed";
      textarea.style.left = "-9999px";
      textarea.style.opacity = "0";
      textarea.setAttribute("readonly", "");
      document.body.appendChild(textarea);
      textarea.focus();
      textarea.select();
      try {
        const ok = document.execCommand("copy");
        document.body.removeChild(textarea);
        if (!ok) throw new Error("execCommand copy failed");
      } catch (err) {
        document.body.removeChild(textarea);
        throw err;
      }
    };

    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        fallbackCopy();
      }
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Copy failed:", err);
      try {
        fallbackCopy();
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      } catch (fallbackErr) {
        console.error("Fallback copy also failed:", fallbackErr);
      }
    }
  };

  return (
    <Tooltip>
      <TooltipTrigger
        render={
          <Button variant="ghost" size="sm" onClick={handleCopy}>
            {copied ? (
              <Check className="w-3 h-3 text-green-600" />
            ) : (
              <Copy className="w-3 h-3" />
            )}
            <span className="ml-1 hidden sm:inline">{copied ? "Copied!" : label}</span>
          </Button>
        }
      />
      <TooltipContent>{copied ? "Copied!" : "Copy to clipboard"}</TooltipContent>
    </Tooltip>
  );
}


