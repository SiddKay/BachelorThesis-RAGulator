<script lang="ts" setup>
import { useQuestionsStore } from "@/stores/questionsStore";
import { storeToRefs } from "pinia";
import { ScrollArea } from "@/components/ui/scroll-area";

const questionsStore = useQuestionsStore();
const { questions } = storeToRefs(questionsStore);
</script>

<template>
  <div class="fixed inset-0 bg-slate-950 flex flex-col">
    <!-- Morphing Gradient as background -->
    <MorphingGradient class="fixed inset-0 z-0" />

    <!-- Main Content in the forefront -->
    <main class="z-10 h-screen m-2 p-2 pt-0 rounded-lg flex flex-col glassmorphism overflow-hidden">
      <!-- Topbar -->
      <MainTopbar class="shrink-0" />

      <!-- Scrollable Area for Questions -->
      <ScrollArea class="flex-grow">
        <div class="p-4 space-y-4">
          <!-- Question Card -->
          <QuestionCard
            v-for="question in questions.slice()"
            :key="question.id"
            :question="question"
          />
        </div>
      </ScrollArea>
    </main>
  </div>
</template>

<style scoped>
.fixed {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
</style>
