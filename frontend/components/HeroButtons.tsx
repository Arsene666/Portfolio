"use client";

import { motion } from "framer-motion";
import { ArrowRight, Download, Mail } from "lucide-react";

export function HeroButtons() {
  return (
    <div className="flex flex-wrap items-center gap-3">
      <motion.a
        href="#projects"
        whileHover={{ scale: 1.03 }}
        whileTap={{ scale: 0.98 }}
        className="hover-elevate flex items-center gap-2 rounded-md bg-accent px-5 py-2.5 text-sm font-medium text-white"
      >
        View My Work
        <ArrowRight size={14} />
      </motion.a>
      <motion.a
        href="/cv.pdf"
        whileHover={{ scale: 1.03 }}
        whileTap={{ scale: 0.98 }}
        className="hover-elevate flex items-center gap-2 rounded-md border border-border px-5 py-2.5 text-sm font-medium text-ink"
      >
        <Download size={14} />
        Download CV
      </motion.a>
      <a
        href="#contact"
        className="hover-elevate flex items-center gap-2 rounded-md px-3 py-2.5 text-sm font-medium text-muted hover:text-ink"
      >
        <Mail size={14} />
        Get In Touch
      </a>
    </div>
  );
}
