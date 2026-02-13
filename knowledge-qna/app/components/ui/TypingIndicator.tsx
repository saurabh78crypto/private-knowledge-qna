import ChatAvatar from "./ChatAvatar";

export default function TypingIndicator() {
  return (
    <div className="flex gap-4">
      <ChatAvatar role="assistant" />

      <div className="bg-white border border-zinc-100 rounded-3xl px-6 py-4 shadow-soft">
        <div className="flex items-center gap-1.5">
          <div
            className="w-2 h-2 bg-zinc-300 rounded-full animate-bounce"
            style={{ animationDelay: "0ms" }}
          />
          <div
            className="w-2 h-2 bg-zinc-300 rounded-full animate-bounce"
            style={{ animationDelay: "150ms" }}
          />
          <div
            className="w-2 h-2 bg-zinc-300 rounded-full animate-bounce"
            style={{ animationDelay: "300ms" }}
          />
        </div>
      </div>
    </div>
  );
}