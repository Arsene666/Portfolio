"use client";

import { useEffect, useState } from "react";

interface Particle {
  left: number;
  top: number;
  scale: number;
}

/** Scattered floating dots behind the hero, matching the reference site's
 * particle field. Positions are randomized once on mount (client-only, to
 * avoid a server/client hydration mismatch from Math.random()). */
export function HeroParticles() {
  const [particles, setParticles] = useState<Particle[]>([]);

  useEffect(() => {
    setParticles(
      Array.from({ length: 30 }, () => ({
        left: Math.random() * 100,
        top: Math.random() * 100,
        scale: 0.5 + Math.random() * 0.7,
      }))
    );
  }, []);

  return (
    <div aria-hidden className="absolute inset-0 overflow-hidden">
      {particles.map((p, i) => (
        <div
          key={i}
          className="absolute h-1 w-1 animate-pulse rounded-full bg-accent/20"
          style={{
            left: `${p.left}%`,
            top: `${p.top}%`,
            transform: `scale(${p.scale})`,
            animationDelay: `${(i % 10) * 0.3}s`,
            animationDuration: "3s",
          }}
        />
      ))}
    </div>
  );
}
