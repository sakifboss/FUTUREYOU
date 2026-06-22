import Link from "next/link";
import { BrainCircuit, History, Library, Settings } from "lucide-react";

const links = [
  { href: "/decisions/new", label: "New", icon: BrainCircuit },
  { href: "/history", label: "History", icon: History },
  { href: "/sources", label: "Sources", icon: Library },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Nav() {
  return (
    <header className="sticky top-0 z-30 border-b border-line bg-paper/90 backdrop-blur dark:border-white/10 dark:bg-midnight/90">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        <Link href="/" className="flex items-center gap-2 font-semibold">
          <span className="grid h-9 w-9 place-items-center rounded-md bg-ink text-paper dark:bg-paper dark:text-ink">
            FY
          </span>
          <span>FutureYou</span>
        </Link>
        <div className="flex items-center gap-1">
          {links.map((link) => {
            const Icon = link.icon;
            return (
              <Link
                key={link.href}
                href={link.href}
                className="inline-flex items-center gap-2 rounded-md px-3 py-2 text-sm text-ink/75 transition hover:bg-black/5 hover:text-ink dark:text-paper/75 dark:hover:bg-white/10 dark:hover:text-paper"
              >
                <Icon className="h-4 w-4" />
                <span className="hidden sm:inline">{link.label}</span>
              </Link>
            );
          })}
        </div>
      </nav>
    </header>
  );
}
