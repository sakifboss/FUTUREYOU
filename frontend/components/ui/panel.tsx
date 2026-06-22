import type { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

export function Panel({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "rounded-lg border border-line bg-white p-5 shadow-sm dark:border-white/10 dark:bg-white/[0.06]",
        className,
      )}
      {...props}
    />
  );
}
