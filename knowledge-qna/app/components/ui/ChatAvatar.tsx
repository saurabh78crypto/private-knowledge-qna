import { User, Bot } from "lucide-react";

interface ChatAvatarProps {
  role: "user" | "assistant";
}

export default function ChatAvatar({ role }: ChatAvatarProps) {
  const isUser = role === "user";

  return (
    <div
      className={`w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center shadow-soft ${
        isUser ? "bg-zinc-700" : "bg-zinc-900"
      }`}
    >
      {isUser ? (
        <User className="w-4 h-4 text-white" />
      ) : (
        <Bot className="w-4 h-4 text-white" />
      )}
    </div>
  );
}