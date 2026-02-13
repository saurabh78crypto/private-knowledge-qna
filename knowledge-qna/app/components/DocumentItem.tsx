import { Calendar, FileText } from "lucide-react";

import { formatUploadDate } from "../lib/helpers";
import { Document } from "@/app/types";

interface DocumentItemProps {
  doc: Document;
}

export default function DocumentItem({ doc }: DocumentItemProps) {
  const formattedDate = formatUploadDate(doc.upload_timestamp);
  
  return (
    <div className="flex items-center gap-3 bg-zinc-50/80 p-3 rounded-xl transition-all hover:bg-zinc-100 hover:shadow-subtle">
      <div className="w-9 h-9 bg-white rounded-xl border border-zinc-200 flex items-center justify-center shadow-subtle">
        <FileText className="w-5 h-5 text-zinc-500" />
      </div>
      
      <div className="flex-1 min-w-0">
        <p className="font-medium text-zinc-800 truncate text-sm">
          {doc.document_name}
        </p>
        <p className="text-xs text-zinc-400 flex items-center gap-1 mt-0.5">
          <Calendar className="w-3 h-3" />
          {formattedDate}
        </p>
      </div>
    </div>
  );
}