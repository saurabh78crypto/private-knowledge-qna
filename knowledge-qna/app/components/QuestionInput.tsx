"use client";

import { useState } from "react";
import { Send } from "lucide-react";

import Button from "./ui/Button";

interface QuestionInputProps {
  onAsk: (q: string) => void;
  isLoading: boolean;
}

export default function QuestionInput({ onAsk, isLoading }: QuestionInputProps) {
  const [question, setQuestion] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (question.trim()) {
      onAsk(question.trim());
      setQuestion("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask anything about your documents..."
        className="flex-1 px-6 py-4 bg-white border border-zinc-200 rounded-2xl 
                   placeholder:text-zinc-400 text-zinc-800
                   focus:outline-none focus:border-zinc-300 focus:ring-2 focus:ring-zinc-100 
                   shadow-subtle transition-all"
        disabled={isLoading}
      />
      <Button type="submit" isLoading={isLoading} variant="primary" className="px-8">
        <Send className="w-5 h-5" />
      </Button>
    </form>
  );
}