"use client";

import { useState, useEffect } from "react";
import { Toaster } from "sonner";

import UploadZone from "./components/UploadZone";
import DocumentList from "./components/DocumentList";
import ChatArea from "./components/ChatArea";
import QuestionInput from "./components/QuestionInput";
import { askQuestion, getDocuments } from "./lib/api";
import { createMessage, getOrCreateGuestId } from "./lib/helpers";
import { Message, Document } from "./types";

export default function Home() {
  const [guestId, setGuestId] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isAsking, setIsAsking] = useState(false);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [docsLoading, setDocsLoading] = useState(true);

  const fetchDocuments = async (id: string) => {
    if (!id) return;
    setDocsLoading(true);
    try {
      const data = await getDocuments(id);
      setDocuments(data);
    } catch (err) {
      console.error("Failed to load documents:", err);
    } finally {
      setDocsLoading(false);
    }
  };

  useEffect(() => {
    const id = getOrCreateGuestId();
    setGuestId(id);
    fetchDocuments(id);
  }, []);

  const handleUploadSuccess = () => {
    fetchDocuments(guestId);
  };

  const handleAsk = async (question: string) => {
    setMessages((prev) => [...prev, createMessage(question, "user")]);

    if (documents.length === 0) {
      setMessages((prev) => [
        ...prev,
        createMessage("Please upload at least one text document first to ask questions.", "assistant"),
      ]);
      return;
    }

    setIsAsking(true);
    try {
      const { answer, sources } = await askQuestion(question, guestId);
      setMessages((prev) => [...prev, createMessage(answer, "assistant", sources)]);
    } catch (err: unknown) {
      setMessages((prev) => [
        ...prev,
        createMessage("I can’t answer at this moment. Please try again later.", "assistant"),
      ]);

      console.error("Ask question error:", err);
    } finally {
      setIsAsking(false);
    }
  };

  return (
    <div className="h-screen bg-zinc-50 flex flex-col lg:flex-row overflow-hidden">
      <Toaster position="top-center" richColors />

      {/* Sidebar */}
      <div className="w-full lg:w-96 bg-white border-b lg:border-r border-zinc-100 flex flex-col lg:flex-shrink-0">
        <div className="px-6 lg:px-8 pt-6 lg:pt-8 pb-5 border-b border-zinc-100">
          <h1 className="text-2xl font-medium tracking-tight text-zinc-900">Private Knowledge</h1>
          <p className="text-sm text-zinc-400 mt-0.5">Your mini workspace</p>
        </div>

        <div className="flex-1 overflow-y-auto p-6 lg:p-8">
          <UploadZone onUploadSuccess={handleUploadSuccess} guestId={guestId} />
          <div className="mt-10">
            <DocumentList documents={documents} loading={docsLoading} />
          </div>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col min-h-0">
        <div className="border-b border-zinc-100 bg-white/80 backdrop-blur-sm px-6 lg:px-8 py-5 flex items-center">
          <h2 className="font-medium text-zinc-800">Ask your documents</h2>
        </div>

        <div className="flex-1 overflow-y-auto p-6 lg:p-8">
          <div className="max-w-3xl mx-auto">
            <ChatArea messages={messages} isLoading={isAsking} />
          </div>
        </div>

        <div className="border-t border-zinc-100 bg-white/80 backdrop-blur-sm p-6 lg:p-8">
          <QuestionInput onAsk={handleAsk} isLoading={isAsking} />
          <p className="text-center text-[10px] text-zinc-400 mt-4 uppercase tracking-wider">
            Only .txt files • Answers are grounded in your documents
          </p>
        </div>
      </div>
    </div>
  );
}