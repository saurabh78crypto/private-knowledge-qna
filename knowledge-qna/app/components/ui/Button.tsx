import { ButtonHTMLAttributes } from "react";
import { Loader2 } from "lucide-react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  isLoading?: boolean;
  variant?: "primary" | "secondary";
}

export default function Button({
  children,
  isLoading,
  variant = "primary",
  ...props
}: ButtonProps) {
  return (
    <button
      disabled={isLoading || props.disabled}
      className={`
        px-6 py-3 rounded-xl font-medium transition-all duration-200 
        flex items-center justify-center gap-2
        focus:outline-none focus:ring-2 focus:ring-zinc-200 focus:ring-offset-2
        disabled:cursor-not-allowed
        ${variant === "primary" 
          ? "bg-zinc-900 text-white hover:bg-zinc-800 disabled:bg-zinc-700 shadow-subtle hover:shadow-soft" 
          : "border border-zinc-200 bg-white text-zinc-700 hover:bg-zinc-50 hover:border-zinc-300 disabled:bg-zinc-50 disabled:text-zinc-400 shadow-subtle"
        }
      `}
      {...props}
    >
      {isLoading && <Loader2 className="w-4 h-4 animate-spin" />}
      {children}
    </button>
  );
}