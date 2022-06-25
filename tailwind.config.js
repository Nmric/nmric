/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './webclient/templates/*.html',
    './webclient/static/**/*.{html,js}',
    './common/plugins/**/*.{py}'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
