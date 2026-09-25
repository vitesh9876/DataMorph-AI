/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0c0e12",
        surface: "#111317",
        "surface-dim": "#111317",
        "surface-container-lowest": "#080a0d",
        "surface-container-low": "#16181d",
        "surface-container": "#1e2026",
        "surface-container-high": "#282a32",
        "surface-container-highest": "#33353f",
        "surface-variant": "#333539",
        "on-surface": "#e2e2e8",
        "on-surface-variant": "#c4c5d9",
        primary: "#b8c3ff",
        "primary-container": "#2e5bff",
        "on-primary": "#002388",
        "on-primary-container": "#efefff",
        secondary: "#c0c1ff",
        "secondary-container": "#3131c0",
        tertiary: "#ddb7ff",
        "tertiary-container": "#943fe2",
        outline: "#8e90a2",
        "outline-variant": "#434656",
        error: "#ffb4ab",
        "error-container": "#93000a",
        success: "#4ade80",
        "success-container": "#064e3b"
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      boxShadow: {
        glow: "0 0 25px -5px rgba(46, 91, 255, 0.4)",
        "glow-lg": "0 0 50px -10px rgba(148, 63, 226, 0.35)",
        "glow-purple": "0 0 35px -5px rgba(184, 195, 255, 0.3)",
        glass: "0 8px 32px 0 rgba(0, 0, 0, 0.37)"
      },
      animation: {
        "pulse-slow": "pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "float": "float 6s ease-in-out infinite",
        "glow": "glow 3s ease-in-out infinite alternate"
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-10px)" },
        },
        glow: {
          "0%": { opacity: 0.4, transform: "scale(0.98)" },
          "100%": { opacity: 0.8, transform: "scale(1.02)" }
        }
      }
    },
  },
  plugins: [],
}
