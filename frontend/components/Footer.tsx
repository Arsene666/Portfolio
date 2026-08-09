export function Footer() {
  return (
    <footer className="border-t border-border py-8">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-3 px-4 sm:flex-row sm:px-8">
        <div className="flex items-center gap-2">
          <span className="font-heading text-sm font-bold">
            arsene<span className="text-accent">.</span>
            <span className="text-muted">ai</span>
          </span>
          <span className="text-xs text-muted">© {new Date().getFullYear()}</span>
        </div>
        <p className="text-xs text-muted">
          Built with FastAPI, Next.js, Qdrant &amp; OpenRouter
        </p>
      </div>
    </footer>
  );
}
