import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0B0F19",
        foreground: "#E2E8F0",
        primary: "#3B82F6",
        quantum: {
          dark: "#0B0F19",
          glow: "#38bdf8",
          accent: "#818cf8"
        }
      },
    },
  },
  plugins: [],
};
export default config;
