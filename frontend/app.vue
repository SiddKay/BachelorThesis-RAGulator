<script lang="ts" setup>
import { useMorphingGradientBgToggleStore } from "@/stores/toggleOpen.store";

const morphingGradientBgToggleStore = useMorphingGradientBgToggleStore();

const route = useRoute();
if (route.path === "/") {
  navigateTo("/sessions");
}
</script>

<template>
  <div class="bg-fixed flex flex-col inset-0 bg-slate-950">
    <!-- Morphing Gradient as background -->
    <MorphingGradient v-if="morphingGradientBgToggleStore.isOpen" class="bg-fixed inset-0 z-0" />

    <!-- Main Content in the forefront -->
    <main class="flex flex-col flex-1 z-10 overflow-hidden">
      <!-- Topbar -->
      <MainTopbar class="flex-shrink-0" />

      <!-- Various pages -->
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>
    </main>
  </div>
</template>

<style scoped>
.bg-fixed {
  position: fixed;
}
</style>
