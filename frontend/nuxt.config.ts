// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  app: {
    head: {
      htmlAttrs: {
        lang: "en"
      },
      title: "RAGulator: LangChain Evaluator",
      meta: [
        {
          name: "viewport",
          content: "width=device-width, initial-scale=1"
        },
        {
          charset: "utf-8"
        }
      ]
    }
  },
  compatibilityDate: "2024-04-03",
  devtools: { enabled: true },

  modules: ["@nuxtjs/tailwindcss", "shadcn-nuxt", "@nuxt/eslint", "@pinia/nuxt"],
  shadcn: {
    /**
     * Prefix for all the imported component
     */
    prefix: "shadcn",
    /**
     * Directory that the component lives in.
     * @default "./components/ui"
     */
    componentDir: "./components/ui"
  },
  pages: true,
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || "http://localhost:8000/v1"
    }
  }
});
