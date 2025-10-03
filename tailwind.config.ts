import type { Config } from 'tailwindcss'

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cricket-green': '#1B5E20',
        'cricket-gold': '#FFD700',
        'cricket-white': '#FFFFFF',
        'cricket-dark': '#333333',
        'cricket-light': '#F5F5F5',
      },
      fontFamily: {
        'cricket': ['Inter', 'Poppins', 'sans-serif'],
        'scoreboard': ['Orbitron', 'monospace'],
      },
      animation: {
        'bounce-slow': 'bounce 2s infinite',
        'pulse-slow': 'pulse 3s infinite',
        'spin-slow': 'spin 3s linear infinite',
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'slide-in-right': 'slideInRight 0.5s ease-out',
        'cricket-ball': 'cricketBall 2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(20px)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        cricketBall: {
          '0%, 100%': { transform: 'rotate(0deg) translateX(0px)' },
          '50%': { transform: 'rotate(180deg) translateX(10px)' },
        },
      },
    },
  },
  plugins: [],
} satisfies Config
