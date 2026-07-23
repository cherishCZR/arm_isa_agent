"use client";

import React from "react";
import { cn } from "@/lib/utils";
import { Bot, User } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  children?: React.ReactNode;
  timestamp?: string;
  className?: string;
}

const markdownComponents: React.ComponentProps<typeof ReactMarkdown>["components"] = {
  code({ className, children, ...props }) {
    const match = /language-(\w+)/.exec(className || "");
    const language = match ? match[1] : "";
    const value = String(children).replace(/\n$/, "");

    if (language) {
      return (
        <SyntaxHighlighter
          style={oneDark as unknown as Record<string, React.CSSProperties>}
          language={language}
          PreTag="div"
          className="rounded-md my-2 text-xs"
        >
          {value}
        </SyntaxHighlighter>
      );
    }

    return (
      <code
        className="bg-muted text-foreground rounded px-1 py-0.5 text-xs font-mono"
        {...props}
      >
        {children}
      </code>
    );
  },
  h1: ({ children }) => <h1 className="text-lg font-bold mt-4 mb-2">{children}</h1>,
  h2: ({ children }) => <h2 className="text-base font-semibold mt-3 mb-2">{children}</h2>,
  h3: ({ children }) => <h3 className="text-sm font-semibold mt-3 mb-1">{children}</h3>,
  p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
  ul: ({ children }) => <ul className="list-disc pl-5 mb-2">{children}</ul>,
  ol: ({ children }) => <ol className="list-decimal pl-5 mb-2">{children}</ol>,
  li: ({ children }) => <li className="mb-0.5">{children}</li>,
  strong: ({ children }) => <strong className="font-semibold text-foreground">{children}</strong>,
  table: ({ children }) => <table className="w-full border-collapse text-xs my-2">{children}</table>,
  thead: ({ children }) => <thead className="bg-muted">{children}</thead>,
  th: ({ children }) => <th className="border px-2 py-1 text-left font-medium">{children}</th>,
  td: ({ children }) => <td className="border px-2 py-1">{children}</td>,
  blockquote: ({ children }) => (
    <blockquote className="border-l-2 border-primary/30 pl-3 italic text-muted-foreground my-2">
      {children}
    </blockquote>
  ),
  hr: () => <hr className="my-3 border-border" />,
  a: ({ href, children }) => (
    <a href={href} target="_blank" rel="noopener noreferrer" className="text-primary underline">
      {children}
    </a>
  ),
};

function MarkdownContent({ content }: { content: string }) {
  return (
    <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
      {content}
    </ReactMarkdown>
  );
}

export function ChatMessage({ role, content, children, timestamp, className }: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <div className={cn("flex gap-3", isUser ? "flex-row-reverse" : "flex-row", className)}>
      {/* Avatar */}
      <div
        className={cn(
          "w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-0.5",
          isUser ? "bg-primary text-primary-foreground" : "bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400"
        )}
      >
        {isUser ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
      </div>

      {/* Bubble */}
      <div className={cn("flex flex-col max-w-[80%]", isUser && "items-end")}>
        <div
          className={cn(
            "rounded-lg px-4 py-2.5 text-sm leading-relaxed",
            isUser
              ? "bg-primary text-primary-foreground"
              : "bg-card border"
          )}
        >
          {content && isUser ? (
            <div className="whitespace-pre-wrap">{content}</div>
          ) : content ? (
            <MarkdownContent content={content} />
          ) : null}
          {children}
        </div>
        {timestamp && (
          <span className="text-[10px] text-muted-foreground mt-0.5 px-1">
            {timestamp}
          </span>
        )}
      </div>
    </div>
  );
}
