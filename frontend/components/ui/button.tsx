import type { ButtonHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost";
};

export function Button({ className, variant = "primary", ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex h-10 items-center justify-center gap-2 rounded-md px-4 text-sm font-semibold transition focus:outline-none focus:ring-2 focus:ring-signal disabled:cursor-not-allowed disabled:opacity-60",
        variant === "primary" && "bg-ink text-paper hover:bg-black dark:bg-paper dark:text-ink",
        variant === "secondary" &&
          "border border-line bg-white text-ink hover:border-ink dark:border-white/15 dark:bg-white/[0.08] dark:text-paper",
        variant === "ghost" && "text-ink hover:bg-black/5 dark:text-paper dark:hover:bg-white/10",
        className,
      )}
      {...props}
    />
  );
}
