# Portfolio frontend

Next.js 14 (App Router) + TypeScript + TailwindCSS + Framer Motion,
connected to the FastAPI backend (projects + streaming RAG chat).

## ⚠️ Critical setup step

**Open this `frontend/` folder itself as the VSCode workspace root — not its parent folder.**

If VSCode is opened on a parent folder that contains both `backend/` and
`frontend/`, it won't find `frontend/tsconfig.json` automatically, and every
`.tsx` file will show red squiggly errors even though the code is correct.
In VSCode: `File > Open Folder...` → select `frontend` directly.

## Setup

```bash
npm install
cp .env.local.example .env.local
npm run dev
```

Make sure the backend is running at the same time, in its own terminal:

```bash
cd ../backend
uvicorn app.main:app --reload
```

Then open `http://localhost:3000`.

## Structure

```
app/
├── globals.css              # Theme tokens (dark-first, .light override), hover-elevate utility
├── layout.tsx                # Fonts, anti-flash theme script, LanguageProvider, ChatWidget
├── page.tsx                  # Assembles all landing page sections
└── projects/[slug]/page.tsx  # Project detail page
components/
├── Header.tsx                 # Fixed nav, scroll-aware background, mobile menu
├── HeroSection.tsx            # Split layout: intro text (left) + ProfilePhoto (right)
├── HeroButtons.tsx            # CTA buttons with Framer Motion micro-interactions
├── ProfilePhoto.tsx           # Rounded photo frame with floating badges (see photo note below)
├── HeroParticles.tsx          # Floating background dots (client-only, avoids hydration mismatch)
├── ProjectsSection.tsx        # Filterable project grid, real images if provided (see note below)
├── AboutSection.tsx           # Bio + animated skill bars
├── JourneySection.tsx         # Alternating vertical timeline
├── ContactSection.tsx         # Contact form (mailto: only — see note below)
├── Footer.tsx
├── ChatWidget.tsx              # Floating RAG chat widget, streams responses via SSE
├── Reveal.tsx                  # Framer Motion scroll-reveal wrapper
├── ThemeToggle.tsx             # Dark/light toggle (persists to localStorage)
├── LanguageToggle.tsx          # EN/FR toggle
└── LanguageContext.tsx         # Language state + translations, shared via React Context
lib/
├── api.ts                    # Typed fetch client (projects + chat, incl. SSE streaming)
├── types.ts
└── i18n.ts                    # Translation dictionary (EN/FR) for all static UI text
```

## Design direction

Built to closely match a specific reference site the user provided,
adapted to the real profile: dark navy background (`#0A0E17`) with a blue
accent (`#3b82f6`), Inter/Space Grotesk/JetBrains Mono via `next/font/google`,
Framer Motion for scroll-reveal and hover/tap micro-interactions, Lucide
icons throughout, and a reusable `.hover-elevate` CSS utility (a subtle
`currentColor` overlay on hover/active) applied to buttons, cards, and
badges for a consistent interaction feel.

## Language switching (EN/FR)

`LanguageContext.tsx` provides `{ lang, setLang, t }` via React Context.
`lib/i18n.ts` holds the full translation dictionary. Any component that
needs translated text calls `const { t } = useLanguage()` and reads from
`t.<section>.<key>`.

**Important limitation:** this only translates *static* UI text (nav
labels, headings, buttons, the chat widget's own labels). It does **not**
translate project content (titles, descriptions) — that comes from the
backend database in whatever language it was written in. Translating that
too would mean adding `title_en`/`title_fr`-style fields to the backend
`Project` model — a separate, bigger change.

The chosen language persists via `localStorage` and updates
`document.documentElement.lang` for accessibility/SEO.

## Add your real photo

`ProfilePhoto.tsx` currently shows initials ("AG") on a gradient inside
the rounded photo frame. To use a real photo:
1. Drop your image at `public/photo.jpg`.
2. In `ProfilePhoto.tsx`, replace the placeholder `<div>` (with the "AG"
   text) with a Next.js `<Image>`:
   ```tsx
   <Image src="/photo.jpg" alt="Arsène Godonou" fill className="object-cover" priority />
   ```
3. Adjust framing if needed with `object-top` / `object-[50%_15%]` /
   `scale-110` classes (crop position and zoom respectively).

## Add real project images

Each project card shows `project.images[0]` if the backend provides one,
falling back to a gradient placeholder otherwise (`ProjectsSection.tsx`).
To add real screenshots:
1. Put image files in `public/projects/`, e.g. `public/projects/rag-assistant.jpg`.
2. In the **backend**, edit `app/db/seed.py` and set the `"images"` field
   for that project: `"images": ["/projects/rag-assistant.jpg"]` (no
   `/public/` prefix).
3. Re-run `python scripts/seed_projects.py` in the backend.

## Known simplification: the contact form

`ContactSection.tsx` opens the visitor's email client with a prefilled
message (`mailto:`) rather than submitting to a backend endpoint. There's
no `/api/v1/contact` route yet — ask if you want that built.

## Verified working

Built and run end-to-end before delivery at each step: `npm run build`
succeeds with 0 TypeScript errors, real screenshots were taken at desktop
and mobile widths in both themes and both languages, hover states and the
language toggle were tested with a real browser automation tool (not just
assumed), and the streaming chat widget was confirmed to receive and
render tokens from a real backend request.