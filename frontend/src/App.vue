<template>
  <RouterView />
</template>

<style>
:root {
  --ink: #14322a;
  --leaf: #2f7d4f;
  --cream: #f6f4ee;
  --muted: #5e6e67;
}
* {
  box-sizing: border-box;
  margin: 0;
}
body {
  font-family: -apple-system, 'Segoe UI', Roboto, Arial, sans-serif;
  background: var(--cream);
  color: var(--ink);
}
</style>
