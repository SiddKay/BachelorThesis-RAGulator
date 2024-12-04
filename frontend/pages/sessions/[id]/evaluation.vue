<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ScrollArea } from "@/components/ui/scroll-area";
import LoadingIndicatorCircularVue from "@/components/LoadingIndicatorCircular.vue";
import { useSessionContext } from "@/composables/useSession";
import { useSessionStore } from "@/stores/sessions.store";
import { useQuestionsStore } from "@/stores/questions.store";

const questionsStore = useQuestionsStore();
const sessionStore = useSessionStore();
const { sessionId } = useSessionContext();
const { allQuestions, isLoading, error } = storeToRefs(questionsStore);

// TODO: Get sessionId dynamically from page context
// const sessionId = ref<UUID>("dd276a29-4cbb-4526-b922-f126827657fb" as UUID);

// Fetch questions when component mounts
onMounted(async () => {
  await sessionStore.fetchSession(sessionId.value);
  await questionsStore.fetchQuestions(sessionId.value);
  console.log("Questions fetched");
});
</script>

<template>
  <section class="flex flex-row flex-1 p-2 pt-0 overflow-hidden">
    <!-- Scrollable Area for Questions -->
    <ScrollArea class="flex-1">
      <div v-if="error" class="p-4 text-center text-red-500">
        {{ error }}
      </div>
      <div v-else-if="allQuestions.length === 0" class="p-4 text-center text-gray-400">
        No questions available. Add some questions to get started.
      </div>
      <!-- TODO: Fix Loading State such that it doesn't block questions -->
      <LoadingIndicatorCircularVue v-if="isLoading" />
      <div v-else class="p-1 space-y-4">
        <QuestionCard
          v-for="question in allQuestions"
          :key="question.id"
          :question="question"
          :session-id="sessionId"
        />
      </div>
    </ScrollArea>

    <!-- Right Sidebar -->
    <RightSidebar />
  </section>
</template>
