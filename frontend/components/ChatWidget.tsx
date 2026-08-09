"use client";

import { useEffect, useRef, useState } from "react";
import { streamChat } from "@/lib/api";
import type { ChatMessage } from "@/lib/types";

const SUGGESTED_QUESTIONS = [
  "Why should I hire Arsène?",
  "What's his best project?",
  "Has he used FastAPI before?",
  "Tell me about his internship",
];

export function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  // One session id per browser tab, kept for the whole visit so the
  // backend's conversation memory (keyed by session_id) actually applies.
  useEffect(() => {
    let id = sessionStorage.getItem("chat-session-id");
    if (!id) {
      id = crypto.randomUUID();
      sessionStorage.setItem("chat-session-id", id);
    }
    setSessionId(id);
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, isLoading]);

  async function sendMessage(text: string) {
    if (!text.trim() || !sessionId || isLoading) return;

    setInput("");
    setIsLoading(true);

    // Push the user message, then an empty assistant placeholder that
    // gets filled in progressively as tokens stream in.
    setMessages((prev) => [
      ...prev,
      { role: "user", content: text },
      { role: "assistant", content: "" },
    ]);

    function updateLastAssistantMessage(update: Partial<ChatMessage>) {
      setMessages((prev) => {
        const next = [...prev];
        const lastIndex = next.length - 1;
        next[lastIndex] = { ...next[lastIndex], ...update };
        return next;
      });
    }

    await streamChat(sessionId, text, {
      onToken: (token) => {
        setMessages((prev) => {
          const next = [...prev];
          const lastIndex = next.length - 1;
          next[lastIndex] = {
            ...next[lastIndex],
            content: next[lastIndex].content + token,
          };
          return next;
        });
      },
      onDone: (sources) => {
        updateLastAssistantMessage({ sources });
        setIsLoading(false);
      },
      onError: () => {
        updateLastAssistantMessage({
          content:
            "Sorry, something went wrong reaching the assistant. Please try again in a moment.",
        });
        setIsLoading(false);
      },
    });
  }

  return (
    <>
      <button
        onClick={() => setIsOpen((v) => !v)}
        aria-label={isOpen ? "Close chat" : "Open chat"}
        className="fixed bottom-5 right-5 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-accent text-white shadow-[0_0_30px_rgba(59,111,240,0.45)] transition hover:scale-105"
      >
        {isOpen ? (
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 6 6 18M6 6l12 12" />
          </svg>
        ) : (
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />
          </svg>
        )}
      </button>

      {isOpen && (
        <div className="fixed bottom-24 right-5 z-50 flex h-[70vh] max-h-[560px] w-[92vw] max-w-sm flex-col overflow-hidden rounded-xl border border-border bg-surface shadow-2xl">
          <div className="border-b border-border px-4 py-3">
            <p className="text-sm font-medium text-ink">Ask about Arsène</p>
            <p className="text-xs text-muted">
              Answers are grounded in his real CV &amp; projects
            </p>
          </div>

          <div ref={scrollRef} className="flex-1 space-y-3 overflow-y-auto px-4 py-4">
            {messages.length === 0 && (
              <div className="space-y-2">
                <p className="text-xs text-muted">Try asking:</p>
                {SUGGESTED_QUESTIONS.map((q) => (
                  <button
                    key={q}
                    onClick={() => sendMessage(q)}
                    className="block w-full rounded-lg border border-border px-3 py-2 text-left text-sm text-ink transition hover:border-accent/60"
                  >
                    {q}
                  </button>
                ))}
              </div>
            )}

            {messages.map((m, i) => (
              <div
                key={i}
                className={m.role === "user" ? "flex justify-end" : "flex justify-start"}
              >
                <div
                  className={
                    m.role === "user"
                      ? "max-w-[85%] rounded-lg bg-accent px-3 py-2 text-sm text-white"
                      : "max-w-[85%] rounded-lg bg-bg px-3 py-2 text-sm text-ink"
                  }
                >
                  {m.role === "assistant" && m.content === "" ? (
                    <p className="text-muted">Thinking…</p>
                  ) : (
                    <p className="whitespace-pre-wrap">{m.content}</p>
                  )}
                  {m.sources && m.sources.length > 0 && (
                    <p className="mt-1.5 text-xs text-muted">
                      Sources: {m.sources.join(", ")}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>

          <form
            onSubmit={(e) => {
              e.preventDefault();
              sendMessage(input);
            }}
            className="flex gap-2 border-t border-border p-3"
          >
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about my background"
              className="flex-1 rounded-lg border border-border bg-bg px-3 py-2 text-sm text-ink outline-none focus:border-accent"
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              aria-label="Send"
              className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-accent text-white disabled:opacity-40"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="m22 2-7 20-4-9-9-4Z" />
                <path d="M22 2 11 13" />
              </svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
}
