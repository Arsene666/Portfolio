import { Award, Mouse } from "lucide-react";
import Image from "next/image"

const TOP_TECH = ["Python", "FastAPI", "PyTorch"];
const BOTTOM_TECH = ["Docker", "Qdrant", "LangChain"];

/** The hero portrait: a rounded photo with floating badge cards around it.
 * Shows initials on a gradient until a real photo is added — see
 * README "Add your real photo" for how to swap it in. */
export function ProfilePhoto() {
  return (
    <div className="relative mx-auto w-full max-w-sm sm:max-w-md">
      {/* Top floating tech pills */}
      <div className="mb-4 flex flex-wrap justify-center gap-2 sm:justify-end sm:pr-6">
        {TOP_TECH.map((tech) => (
          <span
            key={tech}
            className="rounded-full border border-border bg-surface px-3 py-1 text-xs font-medium text-ink shadow-sm"
          >
            {tech}
          </span>
        ))}
      </div>

      <div className="relative">
        {/* The photo itself */}
        <div className="relative aspect-[4/5] overflow-hidden rounded-2xl border border-border shadow-xl">
          {/* Swap this block for a real <Image src="/photo.jpg" .../> once you have one */}
          <div className="flex h-full w-full items-center justify-center bg-gradient-to-br from-accent/25 via-surface to-surface">
            <span className="font-heading text-6xl font-bold text-accent/70"><Image src="/picture.png"alt="Arsène Godonou" fill className="object-cover object-top" priority /></span>
          </div>
        </div>

        {/* Corner badge */}
        <div className="absolute -right-3 -top-3 flex flex-col items-center gap-1 rounded-xl border border-border bg-surface px-4 py-3 text-center shadow-lg sm:-right-5 sm:-top-5">
          <Award className="text-accent" size={22} />
          <span className="text-xs font-semibold text-ink">AI &amp; ML</span>
        </div>

        {/* Stats badge */}
        <div className="absolute -bottom-5 -left-3 rounded-xl border border-border bg-surface px-4 py-3 text-center shadow-lg sm:-left-6">
          <p className="font-heading text-xl font-bold text-ink">5+</p>
          <p className="text-xs text-muted">Projects</p>
        </div>
      </div>

      {/* Bottom floating tech pills */}
      <div className="mt-8 flex flex-wrap justify-center gap-2 sm:justify-start sm:pl-6">
        {BOTTOM_TECH.map((tech) => (
          <span
            key={tech}
            className="rounded-full border border-border bg-surface px-3 py-1 text-xs font-medium text-ink shadow-sm"
          >
            {tech}
          </span>
        ))}
      </div>
    </div>
  );
}

export function ScrollHint() {
  return (
    <div className="mt-16 flex flex-col items-center gap-2 text-muted sm:mt-4">
      <Mouse size={20} className="animate-bounce" />
      <span className="text-xs">Scroll to explore</span>
    </div>
  );
}
