import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// BASE_PATH = /canopia/ per GitHub Pages, / in locale
export default defineConfig({
  base: process.env.BASE_PATH || '/',
  plugins: [vue()],
  test: { environment: 'jsdom' },
});
