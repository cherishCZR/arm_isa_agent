"use client";

import { useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useChatSSE } from "@/lib/hooks/use-chat-sse";
import { useDownload } from "@/lib/hooks/use-download";
import { ChatMessage } from "@/components/chat/chat-message";
import { ChatInput } from "@/components/chat/chat-input";
import { PipelineMini } from "@/components/chat/pipeline-mini-chat";
import { ReasoningCollapse } from "@/components/chat/reasoning-collapse";
import { TestFilesInline } from "@/components/chat/test-files-inline";
import { Play, Trash2, Sparkles } from "lucide-react";

export default function ChatPage() {
  const { messages, pipeline, isStreaming, error, sendMessage, cancel, clearMessages } = useChatSSE();
  const { downloadSingle } = useDownload();
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, pipeline]);

  if (messages.length === 0) {
    return (
      <div className="max-w-2xl mx-auto pt-16">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-purple-100 dark:bg-purple-900/30 mb-4">
            <Sparkles className="w-8 h-8 text-purple-600 dark:text-purple-400" />
          </div>
          <h1 className="text-3xl font-bold mb-2">ARM ISA Copilot</h1>
          <p className="text-muted-foreground">
            Ask me anything about ARM instructions — I can generate test cases, explain encodings, or run the verification pipeline.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-3 mb-8">
          {[
            { title: "Generate test cases", query: "Generate test cases for ADD instruction" },
            { title: "Explain encoding", query: "Explain the encoding format of LDR (immediate)" },
            { title: "Verify instruction", query: "Run verification pipeline for MADD" },
            { title: "Compare instructions", query: "Compare ADD and ADDS - what's different about the flags?" },
          ].map((item) => (
            <Card
              key={item.title}
              className="cursor-pointer hover:border-primary/50 transition-colors"
              onClick={() => sendMessage(item.query)}
            >
              <CardContent className="p-3">
                <p className="text-sm font-medium">{item.title}</p>
                <p className="text-xs text-muted-foreground mt-1 line-clamp-2">{item.query}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        <ChatInput onSend={sendMessage} disabled={isStreaming} />
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto h-[calc(100vh-5rem)] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-4 shrink-0">
        <h1 className="text-lg font-semibold flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-purple-500" />
          ARM ISA Copilot
        </h1>
        <div className="flex gap-2">
          {isStreaming && (
            <Button variant="outline" size="sm" onClick={cancel}>
              Cancel
            </Button>
          )}
          <Button variant="ghost" size="sm" onClick={clearMessages}>
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-auto space-y-4 pr-1">
        {messages.map((msg) => (
          <ChatMessage
            key={msg.id}
            role={msg.role}
            content={msg.content}
            timestamp={msg.timestamp}
          >
            {/* Live pipeline during streaming */}
            {msg.role === "assistant" && msg.isStreaming && pipeline.is_running && (
              <PipelineMini pipeline={pipeline} className="mt-2" />
            )}

            {/* Completed verification result */}
            {msg.role === "assistant" && msg.result && (
              <div className="mt-3 space-y-3">
                {/* Pipeline summary */}
                {msg.result.stage_details.length > 0 && (
                  <ReasoningCollapse stages={msg.result.stage_details} />
                )}

                {/* Test files */}
                {msg.result.test_files.length > 0 && (
                  <TestFilesInline
                    files={msg.result.test_files.filter((f) => f.status === "pass")}
                    onDownload={downloadSingle}
                  />
                )}
              </div>
            )}
          </ChatMessage>
        ))}

        {/* Error */}
        {error && (
          <Card className="border-red-200 bg-red-50 dark:bg-red-950/20">
            <CardContent className="py-2">
              <p className="text-sm text-red-600">{error}</p>
            </CardContent>
          </Card>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="shrink-0 pt-3 border-t mt-3">
        <ChatInput
          onSend={sendMessage}
          disabled={isStreaming}
          placeholder="Ask about ARM instructions, generate tests, or run verification..."
        />
      </div>
    </div>
  );
}
