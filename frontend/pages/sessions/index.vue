<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useSessionStore } from "@/stores/sessions.store";
import SessionCardVue from "~/components/SessionCard.vue";

const sessionStore = useSessionStore();
const { sessions, isLoading, error } = storeToRefs(sessionStore);

// Fetch sessions when component mounts
onMounted(() => {
  sessionStore.fetchSessions();
});
</script>

<template>
  <section class="flex flex-col flex-1 p-4 pt-2 overflow-hidden">
    <ScrollArea class="flex-1">
      <div v-if="error" class="text-red-500">{{ error }}</div>

      <LoadingIndicatorCircular v-if="isLoading" />

      <div v-else-if="sessions.length === 0" class="p-4 text-center text-gray-400">
        No sessions available.
      </div>

      <div v-else class="flex flex-col space-y-4">
        <NuxtLink
          v-for="session in sessions"
          :key="session.id"
          :to="`/sessions/${session.id}/evaluation`"
        >
          <SessionCardVue :session="session" />
        </NuxtLink>
      </div>
    </ScrollArea>
  </section>
</template>
