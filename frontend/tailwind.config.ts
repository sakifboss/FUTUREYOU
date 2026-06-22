import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#101214",
        paper: "#f7f3ec",
        line: "#d9d2c7",
        signal: "#0f766e",
        coral: "#be4b45",
        gold: "#c58b22",
        midnight: "#171b23",
      },
      boxShadow: {
        soft: "0 18px 50px rgba(16, 18, 20, 0.13)",
      },
    },
  },
  plugins: [],
};

export default config;
