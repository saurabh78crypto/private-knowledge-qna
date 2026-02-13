import { Loader2 } from "lucide-react";

interface LoaderProps {
  text?: string;
}

export default function Loader({ text = "Loading..." }: LoaderProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <Loader2 className="w-8 h-8 animate-spin text-zinc-300" />
      <p className="text-zinc-400 mt-3 text-sm font-light">{text}</p>
    </div>
  );
}