/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'gil-blue': '#003C71',
        'gil-red': '#C41E3A',
        'gil-gold': '#FFD700',
      }
    },
  },
  plugins: [],
}
