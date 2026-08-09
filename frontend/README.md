# Portfolio frontend

Next.js 14 (App Router) + TypeScript + TailwindCSS, connected to the FastAPI backend.

## ⚠️ Critical setup step

**Open this `frontend/` folder itself as the VSCode workspace root — not its parent folder.**

## Setup

```bash
npm install
cp .env.local.example .env.local
npm run dev
```

Make sure the backend is running at the same time:

```bash
cd ../backend
uvicorn app.main:app --reload
```

Then open `http://localhost:3000`.

## Structure

```
app/
├── globals.css              # Theme tokens (navy/blue, dark-first, .light override)
├── layout.tsx                # Shared layout + anti-flash theme init + ChatWidget
├── page.tsx                  # Assembles all landing page sections
└── projects/[slug]/page.tsx  # Project detail page
components/
├── Header.tsx                # Sticky nav, theme toggle, resume button
├── HeroSection.tsx           # Hero with animated network background + real stats
├── NetworkBackground.tsx     # Canvas particle-network animation (hero signature element)
├── ProjectsSection.tsx       # Filterable project grid (client component)
├── AboutSection.tsx          # Bio + skill bars (grouped by category)
├── JourneySection.tsx        # Alternating vertical timeline, real CV dates
├── ContactSection.tsx        # Contact form (opens a prefilled email — see note below)
├── Footer.tsx
├── ChatWidget.tsx             # Floating RAG chat widget, streams responses
├── Reveal.tsx                 # Scroll-triggered fade/slide-in wrapper (respects reduced motion)
└── ThemeToggle.tsx            # Dark/light toggle (persists to localStorage)
lib/
├── api.ts                    # Typed fetch client (projects + chat, incl. streaming)
└── types.ts
```

## Design direction

Rebuilt to closely match a specific reference site the user provided
(`portfolio-as.net`), adapted to Arsène's actual profile. Confirmed from the
reference's rendered HTML (fonts, color, and library fingerprints):
- **Fonts**: Inter (body), Space Grotesk (all headings, via `font-heading`),
  JetBrains Mono (tags, stats, percentages, via `font-mono`) — loaded with
  `next/font/google` in `layout.tsx`.
- **Color**: `#3b82f6` (Tailwind's blue-500), taken from the reference's
  favicon SVG.
- **Animation**: Framer Motion (`motion.div` + `whileInView`) instead of a
  hand-rolled IntersectionObserver, matching the reference's animation
  library fingerprint (`opacity:1; transform:none` pattern in its DOM).
- **Icons**: `lucide-react`, matching the reference's icon set exactly
  (confirmed via `class="lucide lucide-sun"` etc. in its markup).
- **Interactions**: a reusable `.hover-elevate` CSS utility (subtle
  currentColor overlay on hover/active) applied to buttons, cards, and
  badges, plus Framer Motion `whileHover`/`whileTap` scale on primary CTAs.
- **Header**: fixed position, transparent at the top, gains a
  background/border once scrolled — plus a real mobile hamburger menu.
- **Journey timeline**: left-aligned with dots on a left line on mobile,
  centered alternating layout from `sm:` up — matching the reference's
  responsive behavior exactly.

## Known simplification: the contact form

`ContactSection.tsx` opens the visitor's email client with a prefilled
message (`mailto:`) rather than submitting to a backend endpoint. There's
no `/api/v1/contact` route yet — ask if you want that built.

## Add your real photo

`components/ProfilePhoto.tsx` currently shows initials ("AG") on a gradient
inside the rounded photo frame. To use a real photo:
1. Drop your image at `public/photo.jpg`.
2. In `ProfilePhoto.tsx`, replace the placeholder `<div>` (with the "AG"
   text) with:
   ```tsx
   <Image src="/photo.jpg" alt="Arsène Godonou" fill className="object-cover" priority />
   ```
   (import `Image` from `next/image` at the top of the file).
3. Adjust `object-position` (e.g. `object-top`) or add a `scale-*` class if
   the framing needs adjusting — same technique used elsewhere in this repo.

## Add real project images

Each project card shows `project.images[0]` if the backend provides one,
falling back to a gradient placeholder otherwise (see `ProjectsSection.tsx`).
To add real screenshots:
1. Put image files in `public/projects/`, e.g. `public/projects/credit-card-fraud-detection.jpg`.
2. In the **backend**, edit `scripts/seed_projects.py` and set the
   `"images"` field for that project, e.g.
   `"images": ["/projects/credit-card-fraud-detection.jpg"]`
   (no `/public/` prefix — see the earlier photo discussion for why).
3. Re-run `python scripts/seed_projects.py` in the backend to update the
   database, then reload the site.

Until real images are added, the gradient + category badge header is the
intentional fallback — not a bug.
