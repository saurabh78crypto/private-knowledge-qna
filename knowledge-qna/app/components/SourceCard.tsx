import { Source } from "@/app/types";

interface SourceCardProps {
  source: Source;
}

export default function SourceCard({ source }: SourceCardProps) {
  return (
    <div className="border-l-2 border-zinc-200 pl-4 py-1 transition-all hover:border-zinc-400 hover:bg-zinc-50 -ml-4 pl-6 pr-2 rounded-r-lg">
      <p className="text-sm font-medium text-zinc-700">{source.document_name}</p>
      <p className="text-sm text-zinc-500 mt-1 line-clamp-2 leading-relaxed">
        {source.excerpt}
      </p>
    </div>
  );
}