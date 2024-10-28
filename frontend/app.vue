<script lang="ts" setup>
import { useQuestionsStore } from "@/stores/questions.store";
import { storeToRefs } from "pinia";
import { ScrollArea } from "@/components/ui/scroll-area";
import LoadingIndicatorCircularVue from "./components/LoadingIndicatorCircular.vue";

const questionsStore = useQuestionsStore();
const { questions, isProcessing } = storeToRefs(questionsStore);

// Fetch questions when component mounts
onMounted(async () => {
  await questionsStore.fetchQuestions();
});
</script>

<template>
  <div class="bg-fixed flex flex-col inset-0 bg-slate-950">
    <!-- Morphing Gradient as background -->
    <MorphingGradient class="bg-fixed inset-0 z-0" />

    <!-- Main Content in the forefront -->
    <div class="flex flex-row flex-1 z-10 overflow-hidden">
      <main class="flex flex-col flex-1 m-2 p-2 pt-0 rounded-lg glassmorphism overflow-hidden">
        <!-- Topbar -->
        <MainTopbar class="flex-shrink-0" />

        <!-- Loading State -->
        <LoadingIndicatorCircularVue v-if="isProcessing" />

        <!-- Scrollable Area for Questions -->
        <ScrollArea v-else class="flex-1">
          <div v-if="questions.length === 0" class="p-4 text-center text-gray-400">
            No questions available. Add some questions to get started.
          </div>
          <div class="p-2 pr-3 space-y-4">
            <!-- Question Card -->
            <QuestionCard v-for="question in questions" :key="question.id" :question="question" />
          </div>
        </ScrollArea>
      </main>

      <!-- Right Sidebar -->
      <RightSidebar />
    </div>
  </div>
</template>

<style scoped>
.bg-fixed {
  position: fixed;
}
</style>
