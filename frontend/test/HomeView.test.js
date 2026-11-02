import { describe, expect, test, vi } from 'vitest';
import { flushPromises, mount } from '@vue/test-utils';
import HomeView from '../src/views/HomeView.vue';

describe('HomeView', () => {
  test('mostra lo stato dell API quando risponde', async () => {
    vi.stubGlobal(
      'fetch',
      vi
        .fn()
        .mockResolvedValue({ ok: true, json: async () => ({ stato: 'ok', versione: '0.1.0' }) }),
    );
    const wrapper = mount(HomeView);
    await flushPromises();
    expect(wrapper.text()).toContain('ok (v0.1.0)');
  });

  test('indica quando l API non è raggiungibile', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('rete')));
    const wrapper = mount(HomeView);
    await flushPromises();
    expect(wrapper.text()).toContain('non raggiungibile');
  });
});
