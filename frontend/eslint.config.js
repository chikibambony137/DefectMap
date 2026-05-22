import globals from "globals";
import pluginVue from "eslint-plugin-vue";
import css from "@eslint/css";
import { defineConfig } from "eslint/config";

export default defineConfig([
  {
    files: ["**/*.{js,mjs,cjs,vue}"],
    languageOptions: { globals: globals.browser },
  },
  pluginVue.configs["flat/essential"],
  { files: ["**/*.css"], plugins: { css }, language: "css/css" },
  {
    ignores: ["dist/**", "build/**", "temp.js", ".quasar/**"],
  },
]);
