import { getProjects } from "@/lib/api";
import { Header } from "@/components/Header";
import { HeroSection } from "@/components/HeroSection";
import { ProjectsSection } from "@/components/ProjectsSection";
import { AboutSection } from "@/components/AboutSection";
import { JourneySection } from "@/components/JourneySection";
import { ContactSection } from "@/components/ContactSection";
import { Footer } from "@/components/Footer";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const projects = await getProjects();

  return (
    <>
      <Header />
      <main>
        <HeroSection />
        <ProjectsSection projects={projects} />
        <AboutSection />
        <JourneySection />
        <ContactSection />
      </main>
      <Footer />
    </>
  );
}
