import type { ChatResponse, Project } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

async function apiFetch<T>(path: string, revalidateSeconds = 60): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    next: { revalidate: revalidateSeconds },
  });

  if (!response.ok) {
    throw new Error(`API request to ${path} failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function getProjects(): Promise<Project[]> {
  return apiFetch<Project[]>("/projects");
}

export function getProject(slug: string): Promise<Project> {
  return apiFetch<Project>(`/projects/${slug}`);
}

export async function postChat(
  sessionId: string,
  message: string
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
  });

  if (!response.ok) {
    throw new Error(`Chat request failed with status ${response.status}`);
  }

  return response.json() as Promise<ChatResponse>;
}

interface StreamCallbacks {
  onToken: (content: string) => void;
  onDone: (sources: string[], confidence: string) => void;
  onError: (message: string) => void;
}

/** Reads the /chat/stream Server-Sent Events response, calling back on
 * each token as it arrives and once more when the stream completes. */
export async function streamChat(
  sessionId: string,
  message: string,
  { onToken, onDone, onError }: StreamCallbacks
): Promise<void> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/chat/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message }),
    });
  } catch {
    onError("Network error while starting the stream.");
    return;
  }

  if (!response.ok || !response.body) {
    onError(`Stream request failed with status ${response.status}`);
    return;
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    // SSE events are separated by a blank line; the last split part may be
    // an incomplete event still waiting for more bytes, so keep it in the buffer.
    const parts = buffer.split("\n\n");
    buffer = parts.pop() ?? "";

    for (const part of parts) {
      const line = part.trim();
      if (!line.startsWith("data: ")) continue;

      try {
        const event = JSON.parse(line.slice("data: ".length));
        if (event.type === "token") {
          onToken(event.content as string);
        } else if (event.type === "done") {
          onDone((event.sources as string[]) ?? [], event.confidence as string);
        }
      } catch {
        // Skip malformed fragments rather than crashing the whole stream.
      }
    }
  }
}
