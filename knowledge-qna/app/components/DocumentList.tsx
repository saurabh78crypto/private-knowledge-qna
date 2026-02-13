"use client";
import { FileText } from "lucide-react";

import Card from "./ui/Card";
import Loader from "./ui/Loader";
import DocumentItem from "./DocumentItem";
import { Document } from "@/app/types";

interface DocumentListProps {
  documents: Document[];
  loading: boolean;
}

export default function DocumentList({ documents, loading }: DocumentListProps) {
  if (loading) return <Loader text="Loading documents..." />;

  return (
    <Card className="shadow-card">
      <h2 className="font-medium text-zinc-800 mb-5 flex items-center gap-2">
        <FileText className="w-5 h-5 text-zinc-500" />
        Your documents{" "}
        <span className="text-zinc-400 text-sm ml-1">({documents.length})</span>
      </h2>
      
      {documents.length === 0 ? (
        <p className="text-zinc-400 text-sm">
          No documents yet. Upload some above.
        </p>
      ) : (
        <div className="space-y-3">
          {documents.map((doc) => (
            <DocumentItem key={doc.document_id} doc={doc} />
          ))}
        </div>
      )}
    </Card>
  );
}