import { notFound } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Github, ExternalLink } from "lucide-react";
import { getProject } from "@/lib/api";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";

export default async function ProjectDetailPage({
  params,
}: {
  params: { slug: string };
}) {
  let project;

  try {
    project = await getProject(params.slug);
  } catch {
    notFound();
  }

  return (
    <>
      <Header />
      <main className="mx-auto min-h-screen max-w-3xl px-4 pb-16 pt-28 sm:px-8 sm:pt-32">
        <Link
          href="/#projects"
          className="hover-elevate inline-flex items-center gap-1.5 rounded-md px-2 py-1 text-sm text-muted hover:text-accent"
        >
          <ArrowLeft size={14} />
          Back to projects
        </Link>

        <div className="mt-6 rounded-xl border border-border bg-surface p-6 sm:p-10">
          <h1 className="font-heading text-2xl font-bold text-ink sm:text-3xl">
            {project.title}
          </h1>
          <div className="mt-3 flex flex-wrap gap-1.5">
            {project.tech_stack.map((tech) => (
              <span
                key={tech}
                className="rounded border border-border px-2 py-0.5 font-mono text-[10px] text-accent"
              >
                {tech}
              </span>
            ))}
          </div>

          <section className="mt-8">
            <h2 className="text-xs font-semibold uppercase tracking-wide text-muted">
              Problem
            </h2>
            <p className="mt-2 text-sm leading-relaxed text-ink">{project.problem_statement}</p>
          </section>

          <section className="mt-6">
            <h2 className="text-xs font-semibold uppercase tracking-wide text-muted">
              Architecture
            </h2>
            <p className="mt-2 text-sm leading-relaxed text-ink">{project.architecture_summary}</p>
          </section>

          <div className="mt-8 flex flex-wrap gap-3">
            {project.github_url && (
              <a
                href={project.github_url}
                className="hover-elevate flex items-center gap-2 rounded-md border border-border px-5 py-2.5 text-sm font-medium text-ink"
              >
                <Github size={16} />
                GitHub
              </a>
            )}
            {project.demo_url && (
              <a
                href={project.demo_url}
                className="hover-elevate flex items-center gap-2 rounded-md bg-accent px-5 py-2.5 text-sm font-medium text-white"
              >
                <ExternalLink size={16} />
                Live demo
              </a>
            )}
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
