"use client";

import { motion } from "framer-motion";
import { MapPin, GraduationCap, Briefcase } from "lucide-react";
import { Reveal } from "./Reveal";

const SKILL_GROUPS = [
  {
    title: "ML & Deep Learning",
    skills: [
      { name: "Scikit-learn", value: 90 },
      { name: "XGBoost", value: 85 },
      { name: "PyTorch", value: 80 },
      { name: "TensorFlow", value: 65 },
    ],
  },
  {
    title: "LLM & NLP",
    skills: [
      { name: "RAG pipelines", value: 85 },
      { name: "LangChain", value: 85 },
      { name: "Prompt engineering", value: 85 },
      { name: "Qdrant / embeddings", value: 80 },
    ],
  },
  {
    title: "Programming",
    skills: [
      { name: "Python", value: 95 },
      { name: "Java", value: 60 },
      { name: "C", value: 55 },
      { name: "R", value: 55 },
    ],
  },
  {
    title: "Backend & Data",
    skills: [
      { name: "FastAPI", value: 90 },
      { name: "Docker", value: 80 },
      { name: "Pandas / NumPy", value: 90 },
      { name: "SQL / MongoDB", value: 75 },
    ],
  },
];

function SkillBar({ name, value }: { name: string; value: number }) {
  return (
    <div>
      <div className="flex items-center justify-between gap-4">
        <span className="text-xs text-muted">{name}</span>
        <span className="font-mono text-[10px] text-muted">{value}%</span>
      </div>
      <div className="relative mt-1.5 h-1.5 w-full overflow-hidden rounded-full bg-border">
        <motion.div
          initial={{ width: 0 }}
          whileInView={{ width: `${value}%` }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="h-full rounded-full bg-accent"
        />
      </div>
    </div>
  );
}

export function AboutSection() {
  return (
    <section id="about" className="border-b border-border bg-surface/50 py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-4 sm:px-8">
        <Reveal>
          <div className="mx-auto max-w-2xl text-center">
            <span className="rounded-md border border-border px-2.5 py-0.5 text-xs font-semibold text-muted">
              About Me
            </span>
            <h2 className="mt-4 font-heading text-3xl font-bold text-ink sm:text-4xl">
              Building AI Systems That Ship
            </h2>
          </div>
        </Reveal>

        <div className="mt-12 grid gap-12 lg:grid-cols-[minmax(0,320px)_1fr]">
          <Reveal delay={100}>
            <div>
              <div className="flex items-start gap-4">
                <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full border-2 border-accent/20 bg-gradient-to-br from-accent/30 to-surface font-heading text-lg font-bold text-accent">
                  AG
                </div>
                <div className="pt-1">
                  <p className="font-heading text-xl font-bold text-ink">Arsène Godonou</p>
                  <p className="text-sm text-muted">AI Engineering Student</p>
                  <p className="mt-1 flex items-center gap-1 text-xs text-muted">
                    <MapPin size={12} /> Calais, France
                  </p>
                </div>
              </div>

              <p className="mt-6 text-sm leading-relaxed text-muted">
                I&apos;m an AI engineering student specialized in data science,
                machine learning, and LLM-based systems. My work spans
                retrieval-augmented pipelines, computer vision, and backend
                engineering — always with an emphasis on shipping something
                real, not just a notebook.
              </p>
              <p className="mt-4 text-sm leading-relaxed text-muted">
                Currently in my second year at EILCO (Calais), on a
                production AI voice-agent internship at Movalib, and looking
                for a one-year apprenticeship (1 month / 1 month rhythm).
              </p>

              <div className="mt-6 flex flex-wrap gap-3">
                <span className="flex items-center gap-1.5 text-xs text-muted">
                  <GraduationCap size={16} className="text-accent" />
                  EILCO — Computer Engineering
                </span>
                <span className="flex items-center gap-1.5 text-xs text-muted">
                  <Briefcase size={16} className="text-accent" />
                  Seeking apprenticeship
                </span>
              </div>
            </div>
          </Reveal>

          <Reveal delay={150}>
            <div>
              <h3 className="mb-6 font-heading text-lg font-bold text-ink">Technical Skills</h3>
              <div className="grid gap-6 sm:grid-cols-2">
                {SKILL_GROUPS.map((group) => (
                  <div key={group.title} className="space-y-3">
                    <h4 className="text-sm font-medium text-ink">{group.title}</h4>
                    <div className="space-y-2.5">
                      {group.skills.map((skill) => (
                        <SkillBar key={skill.name} {...skill} />
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
