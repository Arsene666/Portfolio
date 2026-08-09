import type { Metadata } from "next";
import { Inter, Space_Grotesk, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { ChatWidget } from "@/components/ChatWidget";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });
const spaceGrotesk = Space_Grotesk({ subsets: ["latin"], variable: "--font-heading" });
const jetbrainsMono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" });

export const metadata: Metadata = {
  title: "Arsène Godonou — ML / AI Engineer & Data Scientist",
  description: "Portfolio and interactive AI assistant of Arsène Godonou.",
};

// Runs before React hydrates, so the correct theme class is already on
// <html> by the time anything paints — avoids a flash of the wrong theme.
// Dark is the default brand identity here; light is an explicit opt-in
// the visitor can toggle and which then persists via localStorage.
const themeInitScript = `
(function () {
  var stored = localStorage.getItem("theme");
  var isLight = stored === "light";
  document.documentElement.classList.toggle("light", isLight);
})();
`;

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${spaceGrotesk.variable} ${jetbrainsMono.variable}`}>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeInitScript }} />
      </head>
      <body className="font-sans">
        {children}
        <ChatWidget />
      </body>
    </html>
  );
}
