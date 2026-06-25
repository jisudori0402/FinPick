<template>
  <section class="splash-screen" aria-label="FinPick loading">
    <div class="splash-content">
      <img class="splash-logo" src="@/assets/finpick_logo.png" alt="FinPick" />

      <div class="splash-copy" aria-live="polite">
        <p class="splash-title">금융의 새로운 시작</p>
        <p class="splash-subtitle">내게 필요한 금융부터 Pick하다</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['complete'])

let splashTimer

onMounted(() => {
  splashTimer = window.setTimeout(() => {
    emit('complete')
  }, 4200)
})

onUnmounted(() => {
  window.clearTimeout(splashTimer)
})
</script>

<style scoped>
.splash-screen {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: grid;
  place-items: center;
  overflow: hidden;
  background: #ffffff;
  animation: splashExit 0.86s cubic-bezier(0.4, 0, 0.2, 1) 3.34s forwards;
}

.splash-content {
  width: min(78vw, 360px);
  display: grid;
  justify-items: center;
  gap: 28px;
  transform-origin: center;
  animation: contentLift 4.18s cubic-bezier(0.22, 1, 0.36, 1) forwards;
  will-change: transform, opacity, filter;
}

.splash-logo {
  width: clamp(132px, 30vw, 188px);
  height: auto;
  display: block;
  opacity: 0;
  transform: translateY(10px) scale(0.92);
  filter: blur(10px);
  animation: logoIntro 1.05s cubic-bezier(0.22, 1, 0.36, 1) 0.12s forwards;
}

.splash-copy {
  display: grid;
  justify-items: center;
  gap: 10px;
  text-align: center;
}

.splash-title,
.splash-subtitle {
  margin: 0;
  opacity: 0;
  transform: translateY(18px);
  filter: blur(8px);
  letter-spacing: 0;
  word-break: keep-all;
}

.splash-title {
  color: #111827;
  font-size: clamp(22px, 5vw, 30px);
  line-height: 1.32;
  font-weight: 800;
  animation: textFadeUp 0.9s cubic-bezier(0.22, 1, 0.36, 1) 0.9s forwards;
}

.splash-subtitle {
  color: #14b8a6;
  font-size: clamp(15px, 3.8vw, 18px);
  line-height: 1.5;
  font-weight: 700;
  animation: textFadeUp 0.9s cubic-bezier(0.22, 1, 0.36, 1) 1.72s forwards;
}

@keyframes logoIntro {
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0);
  }
}

@keyframes textFadeUp {
  to {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
  }
}

@keyframes contentLift {
  0%,
  74% {
    opacity: 1;
    transform: scale(1);
    filter: blur(0);
  }

  100% {
    opacity: 0;
    transform: scale(1.045);
    filter: blur(8px);
  }
}

@keyframes splashExit {
  to {
    opacity: 0;
    visibility: hidden;
  }
}

@media (prefers-reduced-motion: reduce) {
  .splash-screen,
  .splash-content,
  .splash-logo,
  .splash-title,
  .splash-subtitle {
    animation-duration: 0.01ms;
    animation-delay: 0ms;
  }
}
</style>
