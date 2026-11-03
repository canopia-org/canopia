import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

async function avvia() {
  // `npm run dev:mock`: API simulate con MSW, senza backend
  if (import.meta.env.MODE === 'mock') {
    const { worker } = await import('./mocks/browser');
    await worker.start({ onUnhandledRequest: 'bypass' });
  }
  createApp(App).use(createPinia()).use(router).mount('#app');
}

avvia();
