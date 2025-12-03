import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 1566,
    proxy: {
      '/upload': 'http://localhost:5888',
      '/query': 'http://localhost:5888',
    }
  }
})
