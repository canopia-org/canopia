<template>
  <main class="home">
    <h1>Canopia</h1>
    <p>Gemello digitale della copertura arborea di Trento.</p>
    <p class="stato">API: {{ statoApi }}</p>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { get } from '../api/client';

const statoApi = ref('verifica in corso…');

onMounted(async () => {
  try {
    const health = await get('/health');
    statoApi.value = `${health.stato} (v${health.versione})`;
  } catch {
    statoApi.value = 'non raggiungibile';
  }
});
</script>

<style scoped>
.home {
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.stato {
  color: var(--muted);
  font-size: 14px;
}
</style>
