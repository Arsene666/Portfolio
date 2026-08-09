import { Briefcase, Award as AwardIcon } from "lucide-react";
import { HeroParticles } from "./HeroParticles";
import { Reveal } from "./Reveal";
import { HeroButtons } from "./HeroButtons";
import { ProfilePhoto, ScrollHint } from "./ProfilePhoto";

const STATS = [
  { icon: Briefcase, label: "5 Projects Completed" },
  { icon: AwardIcon, label: "2 Internships" },
];

export function HeroSection() {
  return (
    <section id="top" className="relative overflow-hidden border-b border-border">
      <div className="absolute inset-0 bg-gradient-to-b from-bg/70 via-bg/85 to-bg" />
      <HeroParticles />

      <div className="relative mx-auto grid max-w-6xl items-center gap-12 px-4 py-28 pt-32 sm:px-8 lg:grid-cols-2 lg:gap-16 lg:py-24 lg:pt-32">
        <div className="text-center lg:text-left">
          <Reveal>
            <span className="inline-flex items-center gap-2 rounded-full border border-border bg-surface px-3 py-1.5 text-xs font-medium text-ink">
              <span className="h-2 w-2 rounded-full bg-accent" />
              Available for a 1-year apprenticeship
            </span>
          </Reveal>

          <Reveal delay={100}>
            <h1 className="mt-6 font-heading text-4xl font-bold leading-tight text-ink sm:text-5xl">
              Hi, I&apos;m Arsène
              <br />
              <span className="text-muted">Godonou</span>
            </h1>
          </Reveal>

          <Reveal delay={150}>
            <p className="mt-3 text-lg font-medium text-accent">
              AI Engineer &amp; Data Scientist
            </p>
          </Reveal>

          <Reveal delay={200}>
            <p className="mx-auto mt-4 max-w-md text-muted lg:mx-0">
              I ship end-to-end AI projects — from imbalanced data science
              problems to retrieval-augmented LLM assistants — combining
              rigorous modeling with production-ready backends.
            </p>
          </Reveal>

          <Reveal delay={250}>
            <div className="mt-6 flex flex-wrap justify-center gap-3 lg:justify-start">
              {STATS.map((stat) => (
                <span
                  key={stat.label}
                  className="flex items-center gap-2 rounded-full border border-border bg-surface px-3 py-1.5 text-xs text-ink"
                >
                  <stat.icon size={14} className="text-accent" />
                  {stat.label}
                </span>
              ))}
            </div>
          </Reveal>

          <Reveal delay={300}>
            <div className="mt-8 flex justify-center lg:justify-start">
              <HeroButtons />
            </div>
          </Reveal>
        </div>

        <Reveal delay={200}>
          <ProfilePhoto />
        </Reveal>
      </div>

      <div className="relative flex justify-center pb-10">
        <ScrollHint />
      </div>
    </section>
  );
}
