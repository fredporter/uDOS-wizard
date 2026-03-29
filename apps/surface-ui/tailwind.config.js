/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,svelte}"],
  theme: {
    extend: {
      colors: {
        canvas: "#efe7db",
        panel: "#fff9f1",
        ink: "#2b241f",
        accent: "#b84a2c",
        line: "#c8b79d",
        muted: "#73614d",
      },
      boxShadow: {
        panel: "0 18px 38px rgba(92, 64, 37, 0.12)",
      },
      fontFamily: {
        display: ['"Fraunces"', "Georgia", "serif"],
        body: ['"IBM Plex Sans"', '"Helvetica Neue"', "sans-serif"],
        prose: ['"Source Serif 4"', "Georgia", "serif"],
        mono: ['"IBM Plex Mono"', "monospace"],
      },
    },
  },
  plugins: [],
};
