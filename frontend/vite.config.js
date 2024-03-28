import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['js-big-decimal']
  },
  server: {
    ...(mode === 'development' && {
      proxy:  {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true
        }
      }
    )
  }
));