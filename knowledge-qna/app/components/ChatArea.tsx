"use client";

import { useEffect, useRef } from "react";
import { Bot } from "lucide-react";

import ChatAvatar from "./ui/ChatAvatar";
import TypingIndicator from "./ui/TypingIndicator";
import SourceCard from "./SourceCard";
import { Message } from "@/app/types";

interface ChatAreaProps {
  messages: Message[];
  isLoading: boolean;
}

export default function ChatArea({ messages, isLoading }: ChatAreaProps) {
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  if (messages.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center py-20">
        <div className="w-20 h-20 bg-zinc-100 rounded-3xl flex items-center justify-center mb-6 shadow-soft">
          <Bot className="w-10 h-10 text-zinc-400" />
        </div>
        <p className="text-2xl font-light text-zinc-400">Your workspace is ready</p>
        <p className="text-zinc-400 mt-2 max-w-xs text-sm">
          Upload documents and start asking questions
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-32">
      {messages.map((msg) => (
        <div key={msg.id} className={`flex gap-4 ${msg.role === "user" ? "justify-end" : ""}`}>

          {msg.role === "assistant" && <ChatAvatar role="assistant" />}

          <div
            className={`max-w-3xl ${
              msg.role === "user"
                ? "bg-zinc-800 text-white shadow-soft"
                : "bg-white border border-zinc-100 shadow-soft"
            } rounded-3xl px-6 py-5`}
          >
            <p className="leading-relaxed whitespace-pre-wrap text-[15px]">{msg.content}</p>

            {msg.sources && msg.sources.length > 0 && (
              <div className="mt-6 pt-6 border-t border-zinc-100">
                <p className="text-xs uppercase tracking-wider text-zinc-400 mb-3 font-medium">
                  Sources
                </p>
                <div className="space-y-4">
                  {msg.sources.map((src, i) => (
                    <SourceCard key={i} source={src} />
                  ))}
                </div>
              </div>
            )}
          </div>

          {msg.role === "user" && <ChatAvatar role="user" />}
          
        </div>
      ))}

      {isLoading && <TypingIndicator />}

      <div ref={chatEndRef} />
    </div>
  );
}