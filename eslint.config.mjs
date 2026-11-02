import js from '@eslint/js';
import globals from 'globals';
import vue from 'eslint-plugin-vue';
import prettier from 'eslint-config-prettier';

export default [
  { ignores: ['**/node_modules/**', '**/dist/**', '**/coverage/**', 'docs/**', 'data/**'] },
  js.configs.recommended,
  {
    files: ['backend/**/*.js'],
    languageOptions: { globals: { ...globals.node, ...globals.jest } },
  },
  ...vue.configs['flat/recommended'],
  {
    files: ['frontend/**/*.{js,vue}'],
    languageOptions: { globals: { ...globals.browser } },
  },
  {
    files: ['frontend/vite.config.js', 'eslint.config.mjs'],
    languageOptions: { globals: { ...globals.node } },
  },
  prettier,
];
