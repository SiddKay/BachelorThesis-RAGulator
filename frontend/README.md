# RAGulator Frontend

The frontend maintains a component based architecture that is built with the [Vue.js](https://vuejs.org/guide/quick-start) (+ [Nuxt.js](https://nuxtjs.org/)) framework, [pinia](https://pinia.vuejs.org/getting-started.html) for component state management of the components, [shadcn-vue](https://www.shadcn-vue.com/docs/installation/nuxt) as the component library and [tailwindcss](https://tailwindcss.com/docs/installation) for the styling.

---

## Quick Start

1. Make sure to install the dependencies:

   ```bash
   npm install
   ```

2. Start the development server on `http://localhost:3000/sessions`:
   ```bash
   npm run dev
   ```
3. Build the application for production and preview it locally:

   ```bash
   npm run build

   npm run preview
   ```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.

## Scripts

| Command            | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| `npm run dev`      | Start development server at `http://localhost:3000/sessions` |
| `npm run lint`     | Run ESLint and Prettier checks                               |
| `npm run lint:fix` | Fix ESLint and Prettier issues                               |
| `npm run build`    | Build for production                                         |
| `npm run preview`  | Preview production build locally                             |
| `npm run generate` | Generate static site                                         |

---

## Directory Structure

```bash
frontend/
├── assets/         # Static assets such as logos & tailwindcss styles
├── components/     # Reusable components used across the frontend
├── composables/    # Connection to the backend via API endpoints
├── utils/          # Utility functions
├── pages/          # Components like sessions and evaluations pages
├── stores/         # Pinia stores for component state management
├── types/          # Schema types analogous to the backend

├── app.vue         # Main application component (entry point)
```
