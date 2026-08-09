"use client";

import { motion } from "framer-motion";
import type { PropsWithChildren } from "react";

/** Fades and slides content into place the first time it scrolls into
 * view — built on Framer Motion's `whileInView`, matching the reference
 * site's animation library. Framer Motion respects prefers-reduced-motion
 * automatically via its built-in MotionConfig defaults on most browsers,
 * but we also gate the initial offset for extra safety. */
export function Reveal({
  children,
  delay = 0,
  className = "",
}: PropsWithChildren<{ delay?: number; className?: string }>) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.6, delay: delay / 1000, ease: "easeOut" }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
