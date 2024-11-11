<script setup lang="ts">
import { useQuestionsStore } from "@/stores/questions.store";
import { storeToRefs } from "pinia";
import { ScrollArea } from "@/components/ui/scroll-area";
import LoadingIndicatorCircularVue from "@/components/LoadingIndicatorCircular.vue";

const questionsStore = useQuestionsStore();
const { questions, isProcessing } = storeToRefs(questionsStore);

// Fetch questions when component mounts
onMounted(async () => {
  await questionsStore.fetchQuestions();
  console.log("Questions fetched");
});
</script>

<template>
  <section class="flex flex-row flex-1 p-2 pt-0 overflow-hidden">
    <!-- Scrollable Area for Questions -->
    <ScrollArea class="flex-1">
      <div v-if="questions.length === 0" class="p-4 text-center text-gray-400">
        No questions available. Add some questions to get started.
      </div>
      <!-- TODO: Fix Loading State such that it doesn't block questions -->
      <LoadingIndicatorCircularVue v-if="isProcessing" />
      <div v-else class="p-1 space-y-4">
        <QuestionCard v-for="question in questions" :key="question.id" :question="question" />
      </div>
    </ScrollArea>

    <!-- Right Sidebar -->
    <RightSidebar />
  </section>
</template>
