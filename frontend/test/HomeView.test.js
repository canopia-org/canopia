import { describe, expect, test } from 'vitest';
import { flushPromises, mount } from '@vue/test-utils';
import { http, HttpResponse } from 'msw';
import { server } from '../src/mocks/server';
import HomeView from '../src/views/HomeView.vue';

const API = 'http://localhost:3000/api/v1';

describe('HomeView', () => {
  test("mostra lo stato dell'API quando risponde", async () => {
    const wrapper = mount(HomeView);
    await flushPromises();
    expect(wrapper.text()).toContain('ok (v0.1.0)');
  });

  test("indica quando l'API non è raggiungibile", async () => {
    server.use(http.get(`${API}/health`, () => HttpResponse.error()));
    const wrapper = mount(HomeView);
    await flushPromises();
    expect(wrapper.text()).toContain('non raggiungibile');
  });
});
