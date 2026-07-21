/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#050B18',
          900: '#081229', // Main background
          850: '#0B1733',
          800: '#10203D', // Card background
          750: '#15284B',
          700: '#1E3A8A', // Glowing border/accent navy
          600: '#2563EB', // Primary action blue
          500: '#3B82F6',
          400: '#60A5FA',
        },
        police: {
          gold: '#D97706',
          badge: '#3B82F6',
          cyan: '#06B6D4',
          emerald: '#10B981',
          crimson: '#EF4444',
          amber: '#F59E0B',
        },
        ksp: {
          bg: '#081229',
          card: '#10203D',
          primary: '#2563EB',
          success: '#22C55E',
          warning: '#F59E0B',
          danger: '#EF4444',
          text: '#F8FAFC',
          muted: '#94A3B8',
          border: 'rgba(59, 130, 246, 0.2)',
        }
      },
      fontFamily: {
        sans: ['Inter', 'Outfit', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
        'neon-blue': '0 0 15px rgba(37, 99, 235, 0.4), 0 0 30px rgba(37, 99, 235, 0.1)',
        'neon-cyan': '0 0 15px rgba(6, 182, 212, 0.4), 0 0 30px rgba(6, 182, 212, 0.1)',
        'neon-red': '0 0 15px rgba(239, 68, 68, 0.4), 0 0 30px rgba(239, 68, 68, 0.1)',
        'glow-sm': '0 0 10px rgba(59, 130, 246, 0.25)',
      },
      backdropBlur: {
        'xs': '2px',
      },
      backgroundImage: {
        'grid-pattern': "radial-gradient(circle, rgba(37, 99, 235, 0.12) 1px, transparent 1px)",
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'cyber-gradient': 'linear-gradient(135deg, rgba(16, 32, 61, 0.9) 0%, rgba(8, 18, 41, 0.95) 100%)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow-pulse': 'glow 2s ease-in-out infinite alternate',
        'scanline': 'scanline 8s linear infinite',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(37, 99, 235, 0.2)' },
          '100%': { boxShadow: '0 0 20px rgba(37, 99, 235, 0.6)' },
        },
        scanline: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(1000%)' },
        }
      }
    },
  },
  plugins: [],
};
