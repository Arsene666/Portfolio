"use client";

import { useEffect, useState } from "react";
import { Download, Menu, X } from "lucide-react";
import { ThemeToggle } from "./ThemeToggle";

const LINKS = [
  { href: "#projects", label: "Projects" },
  { href: "#about", label: "About" },
  { href: "#contact", label: "Contact" },
];

export function Header() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    function onScroll() {
      setScrolled(window.scrollY > 24);
    }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`fixed left-0 right-0 top-0 z-50 transition-all duration-300 ${
        scrolled ? "border-b border-border bg-bg/80 backdrop-blur" : "bg-transparent"
      }`}
    >
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-4 sm:px-8">
        <a href="#top" className="font-heading text-lg font-bold tracking-tight text-ink">
          arsene<span className="text-accent">.</span>
          <span className="text-muted">ai</span>
        </a>

        <nav className="hidden items-center gap-1 sm:flex">
          {LINKS.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="hover-elevate rounded-md px-3 py-2 text-sm text-muted transition-colors hover:text-ink"
            >
              {link.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          <a
            href="/cv.pdf"
            className="hover-elevate hidden items-center gap-2 rounded-md bg-accent px-4 py-2 text-sm font-medium text-white sm:flex"
          >
            <Download size={14} />
            Resume
          </a>
          <button
            onClick={() => setMobileOpen((v) => !v)}
            aria-label={mobileOpen ? "Close menu" : "Open menu"}
            className="hover-elevate flex h-9 w-9 items-center justify-center rounded-md text-ink sm:hidden"
          >
            {mobileOpen ? <X size={18} /> : <Menu size={18} />}
          </button>
        </div>
      </div>

      {mobileOpen && (
        <div className="border-t border-border bg-bg px-4 py-3 sm:hidden">
          <nav className="flex flex-col gap-1">
            {LINKS.map((link) => (
              <a
                key={link.href}
                href={link.href}
                onClick={() => setMobileOpen(false)}
                className="hover-elevate rounded-md px-3 py-2 text-sm text-muted hover:text-ink"
              >
                {link.label}
              </a>
            ))}
            <a
              href="/cv.pdf"
              className="hover-elevate mt-1 flex items-center gap-2 rounded-md bg-accent px-3 py-2 text-sm font-medium text-white"
            >
              <Download size={14} />
              Resume
            </a>
          </nav>
        </div>
      )}
    </header>
  );
}
