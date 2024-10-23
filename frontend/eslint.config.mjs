// @ts-check
import withNuxt from "./.nuxt/eslint.config.mjs";
import eslintConfigPrettier from "eslint-config-prettier";
import prettierPlugin from "eslint-plugin-prettier";
import eslintPluginPrettierRecommended from "eslint-plugin-prettier/recommended";

export default withNuxt({
  plugins: {
    prettier: prettierPlugin
  },
  rules: {
    ...eslintConfigPrettier.rules,
    ...eslintPluginPrettierRecommended.rules,
    // Disable certain rules
    "vue/attribute-hyphenation": "off",
    "vue/require-default-prop": "off",
    "prettier/prettier": [
      "error",
      {
        endOfLine: "auto"
      }
    ]
  },
  files: ["*.vue", "*.ts", "*.css", "*.html"]
});
