import js from '@eslint/js';

export default [
  js.configs.recommended,
  {
    languageOptions: {
      ecmaVersion: 2024,
      sourceType: 'module',
      // node 実行環境の主なグローバル（globals パッケージ非依存で最小限）。
      globals: {
        console: 'readonly',
        process: 'readonly',
        Buffer: 'readonly',
        __dirname: 'readonly',
      },
    },
  },
  {
    ignores: ['node_modules/', 'dist/', '.venv/'],
  },
];
