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

// Fetch questions when component mounts
onMounted(async () => {
  await sessionStore.fetchSession(sessionId.value);
  await questionsStore.fetchQuestions(sessionId.value);
  console.log("Questions fetched");
});
</script>

<template>
  <section class="flex flex-row flex-1 p-4 pt-2 overflow-hidden">
    <!-- Scrollable Area for Questions -->
    <ScrollArea class="flex-1">
      <div v-if="error" class="p-4 text-center text-red-500">
        {{ error }}
      </div>

      <LoadingIndicatorCircularVue v-if="isLoading" />

      <div v-else-if="allQuestions.length === 0" class="p-4 text-center text-gray-400">
        No questions available. Add some questions to get started.
      </div>

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
