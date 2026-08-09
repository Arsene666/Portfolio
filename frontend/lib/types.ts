export interface Project {
  id: number;
  slug: string;
  title: string;
  short_description: string;
  problem_statement: string;
  architecture_summary: string;
  tech_stack: string[];
  github_url: string | null;
  demo_url: string | null;
  demo_slug: string | null;
  images: string[];
  is_featured: boolean;
  created_at: string;
}

export interface ChatResponse {
  answer: string;
  sources: string[];
  confidence: "high" | "low" | "no_context";
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
}
