<script setup lang="ts">
import { useSessionStore } from "@/stores/sessions.store";
import { storeToRefs } from "pinia";

const sessionStore = useSessionStore();
const { sessions, isLoading, error } = storeToRefs(sessionStore);

// Fetch sessions when component mounts
onMounted(() => {
  sessionStore.fetchSessions();
});
</script>

<template>
  <section class="container mx-auto p-6">
    <h1 class="text-gray-200 text-2xl font-bold mb-6">Sessions</h1>
    <div class="grid gap-4">
      <div v-if="error" class="text-red-500">{{ error }}</div>
      <LoadingIndicatorCircular v-if="isLoading" />
      <div v-else-if="sessions.length === 0" class="text-gray-400">No sessions available.</div>
      <NuxtLink
        v-for="session in sessions"
        :key="session.id"
        :to="`/sessions/${session.id}/evaluation`"
        class="p-4 border rounded-lg glassmorphism hover:glassmorphism-modal"
      >
        <h2 class="font-semibold">{{ session.name }}</h2>
        <p class="text-sm text-gray-400">{{ session.description }}</p>
      </NuxtLink>
    </div>
  </section>
</template>
