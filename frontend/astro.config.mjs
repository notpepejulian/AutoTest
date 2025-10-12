import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import node from '@astrojs/node';

export default defineConfig({
  integrations: [tailwind()],
  output: 'hybrid',  // Permite mezclar páginas estáticas y SSR
  adapter: node({
    mode: 'standalone'
  }),
  server: {
    host: true,
    port: 4321
  }
});
