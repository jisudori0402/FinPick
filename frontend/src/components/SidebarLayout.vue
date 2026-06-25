<template>
  <section class="sidebar-layout" :class="surfaceClass">
    <aside class="sidebar-layout__sidebar">
      <slot name="sidebar"></slot>
    </aside>

    <main class="sidebar-layout__content">
      <slot></slot>
    </main>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  surface: {
    type: String,
    default: 'soft',
    validator: (value) => ['soft', 'white'].includes(value),
  },
})

const surfaceClass = computed(() => `sidebar-layout--${props.surface}`)
</script>
