<template>
  <div class="app-sidebar">
    <div class="app-sidebar__top">
      <slot name="top"></slot>
    </div>

    <div class="app-sidebar__nav">
      <slot name="nav"></slot>
    </div>

    <div class="app-sidebar__support">
      <slot name="support"></slot>
    </div>
  </div>
</template>
