"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Send } from "lucide-react";
import { Reveal } from "./Reveal";

const CONTACT_EMAIL = "godonouarsene18@gmail.com";

export function ContactSection() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [company, setCompany] = useState("");
  const [message, setMessage] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const subject = encodeURIComponent(
      company ? `Opportunity from ${company}` : "Let's talk"
    );
    const body = encodeURIComponent(
      `${message}\n\n— ${name} (${email})${company ? `\n${company}` : ""}`
    );

    window.location.href = `mailto:${CONTACT_EMAIL}?subject=${subject}&body=${body}`;
  }

  return (
    <section id="contact" className="py-20 sm:py-28">
      <div className="mx-auto max-w-lg px-4 text-center sm:px-8">
        <Reveal>
          <span className="rounded-md border border-border px-2.5 py-0.5 text-xs font-semibold text-muted">
            Get In Touch
          </span>
          <h2 className="mt-4 font-heading text-3xl font-bold text-ink sm:text-4xl">
            Let&apos;s Build Something Together
          </h2>
          <p className="mt-4 text-muted">
            Interested in an apprenticeship or ML engineering role? I&apos;d
            love to hear from you.
          </p>
        </Reveal>

        <Reveal delay={100}>
          <form
            onSubmit={handleSubmit}
            className="mt-10 rounded-xl border border-border bg-surface p-6 text-left"
          >
            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label className="text-sm font-medium text-ink" htmlFor="name">
                  Name *
                </label>
                <input
                  id="name"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Your name"
                  className="mt-1.5 w-full rounded-md border border-border bg-bg px-3 py-2 text-sm text-ink outline-none transition-colors focus:border-accent"
                />
              </div>
              <div>
                <label className="text-sm font-medium text-ink" htmlFor="email">
                  Email *
                </label>
                <input
                  id="email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@company.com"
                  className="mt-1.5 w-full rounded-md border border-border bg-bg px-3 py-2 text-sm text-ink outline-none transition-colors focus:border-accent"
                />
              </div>
            </div>

            <div className="mt-4">
              <label className="text-sm font-medium text-ink" htmlFor="company">
                Company
              </label>
              <input
                id="company"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                placeholder="Your company (optional)"
                className="mt-1.5 w-full rounded-md border border-border bg-bg px-3 py-2 text-sm text-ink outline-none transition-colors focus:border-accent"
              />
            </div>

            <div className="mt-4">
              <label className="text-sm font-medium text-ink" htmlFor="message">
                Message *
              </label>
              <textarea
                id="message"
                required
                rows={4}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Tell me about the opportunity or what you'd like to discuss..."
                className="mt-1.5 w-full rounded-md border border-border bg-bg px-3 py-2 text-sm text-ink outline-none transition-colors focus:border-accent"
              />
            </div>

            <motion.button
              type="submit"
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.98 }}
              className="hover-elevate mt-6 flex w-full items-center justify-center gap-2 rounded-md bg-accent px-4 py-2.5 text-sm font-medium text-white"
            >
              <Send size={16} />
              Send Message
            </motion.button>
          </form>
        </Reveal>
      </div>
    </section>
  );
}
