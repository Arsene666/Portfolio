import { Reveal } from "./Reveal";

const MILESTONES = [
  {
    year: "2021–2023",
    title: "Classes Préparatoires (MP)",
    description: "Intensive math & physics prep track — IMSP, Benin.",
  },
  {
    year: "2023–2024",
    title: "Mathematics Degree",
    description: "Special mathematics licence — IMSP, Benin.",
  },
  {
    year: "2024",
    title: "Data Analyst Internship",
    description:
      "Benin Digital — cleaned and modeled multi-source data, built Power BI dashboards.",
  },
  {
    year: "2025",
    title: "Computer Engineering — EILCO",
    description: "Started 2nd year of the AI engineering track in Calais, France.",
  },
  {
    year: "2025–2026",
    title: "AI / ML Engineer Internship",
    description:
      "Movalib — designed and deployed an autonomous AI voice agent (FastAPI, LLMs, telephony stack).",
  },
  {
    year: "2026+",
    title: "Seeking a 1-Year Apprenticeship",
    description: "Targeting ML/AI engineering or backend Python roles.",
  },
];

export function JourneySection() {
  return (
    <section className="border-b border-border py-20 sm:py-28">
      <div className="mx-auto max-w-3xl px-4 sm:px-8">
        <Reveal>
          <h2 className="text-center font-heading text-3xl font-bold text-ink sm:text-4xl">
            Journey
          </h2>
        </Reveal>

        <div className="relative mx-auto mt-16">
          <div className="absolute bottom-0 left-4 top-0 w-px bg-border sm:left-1/2 sm:-translate-x-px" />

          <div className="space-y-8">
            {MILESTONES.map((milestone, i) => {
              const isEven = i % 2 === 0;
              return (
                <Reveal key={milestone.title} delay={(i % 4) * 100}>
                  <div
                    className={`relative flex items-start gap-4 pl-10 sm:pl-0 ${
                      isEven ? "sm:flex-row sm:text-right" : "sm:flex-row-reverse sm:text-left"
                    }`}
                  >
                    <div className={`flex-1 ${isEven ? "sm:pr-8" : "sm:pl-8"}`}>
                      <span className="mb-1 inline-block rounded-md border border-border px-2 py-0.5 font-mono text-[10px] font-medium text-muted">
                        {milestone.year}
                      </span>
                      <h3 className="text-sm font-medium text-ink">{milestone.title}</h3>
                      <p className="mt-0.5 text-xs text-muted">{milestone.description}</p>
                    </div>

                    <span className="absolute left-2.5 mt-1.5 h-3 w-3 rounded-full border-2 border-bg bg-accent sm:left-1/2 sm:-translate-x-1/2" />

                    <div className="hidden flex-1 sm:block" />
                  </div>
                </Reveal>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
