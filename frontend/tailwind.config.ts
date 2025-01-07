// frontend/tailwind.config.ts

/** @type {import('tailwindcss').Config} */
const config = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    "./public/**/*.html",
  ],
  theme: {
    extend: {
      keyframes: {
        'move-left': {
          '0%': { transform: 'translate(0, 0) rotate(0deg)', opacity: '1' },
          '100%': { transform: 'translate(-100px, -100px) rotate(-360deg)', opacity: '0' },
        },
        'move-right': {
          '0%': { transform: 'translate(0, 0) rotate(0deg)', opacity: '1' },
          '100%': { transform: 'translate(100px, -100px) rotate(360deg)', opacity: '0' },
        },
      },
      animation: {
        'move-left': 'move-left linear infinite',
        'move-right': 'move-right linear infinite',
      },
      colors: {
        'neon-red': '#FF0000',
        'neon-blue': '#00FFFF',
      },
    },
  },
  plugins: [],
};

export default config;
