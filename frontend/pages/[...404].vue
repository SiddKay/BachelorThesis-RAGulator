<script setup lang="ts">
import { RouterLink } from "vue-router";
import { TriangleAlert } from "lucide-vue-next";
import { Button } from "@/components/ui/button";
</script>

<template>
  <section
    class="text-center text-gray-300 flex flex-col justify-center items-center w-full h-full"
  >
    <TriangleAlert class="text-yellow-500 mb-5 size-14" />
    <h1 class="text-4xl font-bold mb-4">404 Not Found</h1>
    <p class="text-lg">This page does not exist.</p>
    <p class="text-lg mb-5">Please check the URL.</p>
    <RouterLink to="/evaluation">
      <Button
        size="lg"
        variant="ghost"
        class="text-md text hover:glassmorphism hover:border-none select-none"
        aria-label="Go Back"
      >
        Go Back
      </Button>
    </RouterLink>
  </section>
</template>
