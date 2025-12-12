import stylistic from '@stylistic/eslint-plugin';
import { defineConfig } from 'eslint/config';
import nextVitals from 'eslint-config-next/core-web-vitals';
import nextTs from 'eslint-config-next/typescript';

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  { files: ['**/*.{js,mjs,cjs,ts,tsx,jsx}'] },
  {
    plugins: {
      '@stylistic': stylistic
    },
    rules: {
      '@stylistic/indent': ['error', 2],
      '@stylistic/no-tabs': ['error'],
      '@stylistic/max-len': ['error', { 'code': 80, 'ignoreStrings': true, 'tabWidth': 2, 'ignoreComments': true }],
      '@stylistic/quotes': ['error', 'single'],
      '@stylistic/eol-last': ['error', 'always'],
      '@stylistic/no-multiple-empty-lines': ['error', { 'max': 1, 'maxEOF': 0 }],
      '@stylistic/semi': ['error', 'always'],
      '@stylistic/no-multi-spaces': ['error'],
      '@stylistic/curly-newline': ['error', { 'consistent': true }],
      '@stylistic/object-curly-spacing': ['error', 'always'],
      '@stylistic/no-trailing-spaces': ['error'],
    }
  }
]);

export default eslintConfig;
