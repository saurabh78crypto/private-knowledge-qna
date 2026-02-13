"use client";

import { useState, useRef } from "react";
import { Upload, Loader2 } from "lucide-react";
import { toast } from "sonner";

import { uploadDocuments } from "@/app/lib/api";

interface UploadZoneProps {
  onUploadSuccess: () => void;
  guestId: string;
}

export default function UploadZone({ onUploadSuccess, guestId }: UploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleUpload = async (files: FileList | File[]) => {
    const txtFiles = Array.from(files).filter(f => f.name.endsWith(".txt"));
    if (txtFiles.length === 0) return toast.error("Only .txt files are allowed");

    setIsUploading(true);
    try {
      await uploadDocuments(txtFiles, guestId);
      toast.success(`${txtFiles.length} document(s) uploaded successfully`);
      onUploadSuccess();
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : "Upload failed";
      toast.error(errorMessage);
    } finally {
      setIsUploading(false);
    }
  };

  const openFileDialog = () => {
    if (!isUploading) fileInputRef.current?.click();
  };

  return (
    <>
      <div
        onClick={openFileDialog}
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={(e) => { e.preventDefault(); setIsDragging(false); handleUpload(e.dataTransfer.files); }}
        className={`
          border-2 border-dashed rounded-3xl p-10 text-center transition-all duration-200 cursor-pointer
          flex flex-col items-center justify-center
          ${isDragging 
            ? "border-zinc-800 bg-zinc-50/50 shadow-soft" 
            : "border-zinc-200 hover:border-zinc-300 bg-white hover:shadow-soft"
          }
        `}
      >
        <div className="mx-auto w-16 h-16 bg-zinc-100 rounded-2xl flex items-center justify-center mb-5 shadow-subtle">
          {isUploading ? (
            <Loader2 className="w-8 h-8 text-zinc-400 animate-spin" />
          ) : (
            <Upload className="w-8 h-8 text-zinc-400" />
          )}
        </div>
        <p className="text-xl font-light text-zinc-700">
          {isUploading ? "Uploading..." : "Upload or Drop"}
        </p>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".txt"
        className="hidden"
        onChange={(e) => e.target.files && handleUpload(e.target.files)}
      />
    </>
  );
}