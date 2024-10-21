<script lang="ts" setup>
import MorphingGradient from "@/components/MorphingGradient.vue";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
</script>

<template>
  <main class="relative w-screen h-screen bg-neutral-950 flex items-center justify-center">
    <!-- Morphing Gradient as background -->
    <MorphingGradient class="absolute inset-0 z-0" />

    <!-- Centered Card with Glassmorphism Effect -->
    <Card class="relative z-10 w-[250px] min-h-[100px] flex-shrink-0 bg-glassmorphic">
      <CardHeader class="flex flex-row items-center justify-between space-y-0 p-2">
        <CardTitle class="text-sm font-medium text-gray-300">Answer ABC</CardTitle>
      </CardHeader>

      <!-- Answer card content -->
      <CardContent class="p-2.5 overflow-y-auto overflow-ellipsis">
        <p class="text text-gray-200">HOLLLAAAAAA</p>
      </CardContent>
    </Card>
  </main>
</template>

<style scoped>
.absolute {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.bg-glassmorphic {
  background: rgba(255, 255, 255, 0.1); /* Slight transparency */
  backdrop-filter: blur(10px); /* Glass effect */
  border: 1px solid rgba(255, 255, 255, 0.2); /* Frosted border */
  border-radius: 12px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2); /* Subtle shadow */
}
</style>
