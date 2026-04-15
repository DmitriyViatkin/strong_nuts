import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  root: resolve(__dirname, 'src'),
  base: '/static/dist/',
  build: {
    outDir: resolve(__dirname, '../static/dist'),
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'src/js/main.js'),
      }
    },
    assetsDir: 'assets',
  },
  server: {
    host: 'localhost',
    port: 5173,
    hmr: { host: 'localhost' },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@sass': resolve(__dirname, 'src/sass'),
      '@js': resolve(__dirname, 'src/js'),
      '@img': resolve(__dirname, 'src/img'),
      '@fonts': resolve(__dirname, 'src/fonts'),
    }
  }
})
