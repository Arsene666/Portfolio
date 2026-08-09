"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { Github, ArrowRight } from "lucide-react";
import type { Project } from "@/lib/types";
import { Reveal } from "./Reveal";

const CATEGORY_BY_SLUG: Record<string, string> = {
  "credit-card-fraud-detection": "Data Science",
  "rag-assistant": "RAG & LLM",
  "object-detection-api": "Computer Vision",
  "agro-ia-postharvest": "Embedded / IoT",
  "rag-portfolio-assistant": "RAG & LLM",
};

const METRIC_BY_SLUG: Record<string, { value: string; label: string }> = {
  "credit-card-fraud-detection": { value: "97%", label: "Precision" },
  "rag-assistant": { value: "RAG", label: "End-to-end pipeline" },
  "object-detection-api": { value: "0.64", label: "mAP" },
  "agro-ia-postharvest": { value: "IoT", label: "Prototype" },
  "rag-portfolio-assistant": { value: "Live", label: "On this site" },
};

const GRADIENT_BY_CATEGORY: Record<string, string> = {
  "Data Science": "from-accent/25 via-surface to-surface",
  "RAG & LLM": "from-gold/20 via-surface to-surface",
  "Computer Vision": "from-accent/30 via-accent/5 to-surface",
  "Embedded / IoT": "from-gold/15 via-surface to-surface",
};

function getCategory(project: Project): string {
  return CATEGORY_BY_SLUG[project.slug] ?? "Other";
}

export function ProjectsSection({ projects }: { projects: Project[] }) {
  const categories = ["All", ...Array.from(new Set(projects.map(getCategory)))];
  const [active, setActive] = useState("All");

  const visible =
    active === "All" ? projects : projects.filter((p) => getCategory(p) === active);

  return (
    <section id="projects" className="border-b border-border py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-4 sm:px-8">
        <Reveal>
          <div className="mx-auto max-w-2xl text-center">
            <span className="rounded-md border border-border px-2.5 py-0.5 text-xs font-semibold text-muted">
              Featured Work
            </span>
            <h2 className="mt-4 font-heading text-3xl font-bold text-ink sm:text-4xl">
              AI &amp; ML Projects
            </h2>
            <p className="mt-4 text-muted">
              Real problems worked end to end — data exploration, modeling,
              and where relevant, a real API around the model.
            </p>
          </div>
        </Reveal>

        <Reveal delay={100}>
          <div className="mt-8 flex flex-wrap justify-center gap-2">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setActive(cat)}
                className={
                  active === cat
                    ? "hover-elevate rounded-md bg-accent px-3 py-1.5 text-xs font-medium text-white"
                    : "hover-elevate rounded-md border border-border px-3 py-1.5 text-xs text-muted hover:text-ink"
                }
              >
                {cat}
              </button>
            ))}
          </div>
        </Reveal>

        <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {visible.map((project, i) => {
            const category = getCategory(project);
            const metric = METRIC_BY_SLUG[project.slug];
            const gradient = GRADIENT_BY_CATEGORY[category] ?? "from-accent/15 to-surface";

            return (
              <Reveal key={project.slug} delay={(i % 3) * 100}>
                <div className="group overflow-hidden rounded-xl border border-border bg-surface transition-all duration-300 hover:-translate-y-1 hover:border-accent/60 hover:shadow-[0_10px_40px_-10px_rgba(59,130,246,0.35)]">
                  <div className="relative aspect-video overflow-hidden">
                    {project.images[0] ? (
                      <Image
                        src={project.images[0]}
                        alt={project.title}
                        fill
                        sizes="(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"
                        className="object-cover transition-transform duration-500 group-hover:scale-105"
                      />
                    ) : (
                      <div className={`h-full w-full bg-gradient-to-br ${gradient}`} />
                    )}
                    <div className="absolute inset-0 bg-gradient-to-t from-bg/85 to-transparent" />
                    <div className="absolute inset-x-3 bottom-3 flex items-end justify-between gap-2">
                      <span className="rounded-md bg-bg/70 px-2 py-1 text-xs font-medium text-ink">
                        {category}
                      </span>
                      {metric && (
                        <div className="text-right transition-transform duration-300 group-hover:-translate-y-1">
                          <p className="font-heading text-lg font-bold text-ink">{metric.value}</p>
                          <p className="text-[10px] text-muted">{metric.label}</p>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="p-4">
                    <h3 className="font-heading font-bold text-ink transition-colors group-hover:text-accent">
                      {project.title}
                    </h3>
                    <p className="mt-2 line-clamp-2 text-sm leading-relaxed text-muted">
                      {project.short_description}
                    </p>

                    <div className="mt-3 flex flex-wrap gap-1.5">
                      {project.tech_stack.slice(0, 4).map((tech) => (
                        <span
                          key={tech}
                          className="rounded border border-border px-2 py-0.5 font-mono text-[10px] text-muted"
                        >
                          {tech}
                        </span>
                      ))}
                      {project.tech_stack.length > 4 && (
                        <span className="rounded border border-border px-2 py-0.5 text-[10px] text-muted">
                          +{project.tech_stack.length - 4}
                        </span>
                      )}
                    </div>

                    <div className="mt-4 flex items-center justify-between text-xs">
                      {project.github_url ? (
                        <a
                          href={project.github_url}
                          className="hover-elevate flex items-center gap-1.5 rounded-md px-3 py-2 text-muted transition-colors hover:text-ink"
                        >
                          <Github size={14} />
                          Code
                        </a>
                      ) : (
                        <span />
                      )}
                      <Link
                        href={`/projects/${project.slug}`}
                        className="hover-elevate flex items-center gap-1 rounded-md px-3 py-2 font-medium text-accent"
                      >
                        Details
                        <ArrowRight size={14} className="transition-transform group-hover:translate-x-1" />
                      </Link>
                    </div>
                  </div>
                </div>
              </Reveal>
            );
          })}
        </div>
      </div>
    </section>
  );
}
