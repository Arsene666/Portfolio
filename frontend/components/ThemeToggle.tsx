"use client";

import { useEffect, useState } from "react";
import { Sun, Moon } from "lucide-react";

export function ThemeToggle() {
  const [isLight, setIsLight] = useState(false);

  // Sync local state with whatever the inline init script (in layout.tsx)
  // already applied to <html> on first paint, so the icon matches reality.
  useEffect(() => {
    setIsLight(document.documentElement.classList.contains("light"));
  }, []);

  function toggle() {
    const next = !isLight;
    setIsLight(next);
    document.documentElement.classList.toggle("light", next);
    localStorage.setItem("theme", next ? "light" : "dark");
  }

  return (
    <button
      onClick={toggle}
      aria-label={isLight ? "Switch to dark mode" : "Switch to light mode"}
      className="hover-elevate flex h-9 w-9 items-center justify-center rounded-md text-ink transition-colors hover:text-accent"
    >
      {isLight ? <Moon size={16} /> : <Sun size={16} />}
    </button>
  );
}
