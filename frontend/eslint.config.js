import js from "@eslint/js";
import globals from "globals";
import pluginVue from "eslint-plugin-vue";
import vueParser from "vue-eslint-parser";
import { defineConfig } from "eslint/config";
import prettierConfig from "eslint-config-prettier";

export default defineConfig([

  prettierConfig, // отключает правила, которые конфликтуют с Prettier

  // 1. Игнорируемые файлы (аналог .eslintignore)
  {
    ignores: [
      "node_modules/**",
      "dist/**",
      "build/**",
      "*.config.js",
      "*.config.ts",
      ".eslintrc.*",
      "coverage/**"
    ]
  },

  // 2. Базовые настройки для всех файлов
  {
    files: ["**/*.{js,mjs,cjs,vue}"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.es2021
      },
      // ВАЖНО: указываем парсер для Vue файлов
      parser: vueParser,
      parserOptions: {
        parser: js,  // используем импортированный модуль
        sourceType: "module",
        ecmaVersion: "latest"
      }
    },
    plugins: {
      js: js
    },
    rules: {
      // Рекомендованные правила JS
      ...js.configs.recommended.rules,
      
      // Кастомные правила
      "no-console": process.env.NODE_ENV === "production" ? "error" : "warn",
      "no-debugger": process.env.NODE_ENV === "production" ? "error" : "warn",
      "no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
      "semi": ["error", "always"],
      "quotes": ["error", "single", { avoidEscape: true }],
      "comma-dangle": ["error", "never"],
      "indent": ["error", 2, { SwitchCase: 1 }],
      "space-before-function-paren": ["error", "never"],
      "object-curly-spacing": ["error", "always"],
      "array-bracket-spacing": ["error", "never"],
      "no-multiple-empty-lines": ["error", { max: 1 }],
      "eol-last": ["error", "always"]
    }
  },

  // 3. Специальные настройки для Vue файлов
  ...pluginVue.configs["flat/essential"].map(config => ({
    ...config,
    files: ["**/*.vue"],
    rules: {
      ...config.rules,
      // Vue специфичные правила
      "vue/multi-word-component-names": "off",
      "vue/no-v-html": "warn",
      "vue/require-default-prop": "off",
      "vue/attribute-hyphenation": ["error", "always"],
      "vue/html-indent": ["error", 2],
      "vue/max-attributes-per-line": ["error", {
        singleline: 3,
        multiline: 1
      }]
    }
  }))
]);