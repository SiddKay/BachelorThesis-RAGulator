<script lang="ts" setup>
import { useQuestionsStore } from "@/stores/questionsStore";
import { storeToRefs } from "pinia";
import { ScrollArea } from "@/components/ui/scroll-area";

const questionsStore = useQuestionsStore();
const { questions } = storeToRefs(questionsStore);
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

        <!-- Scrollable Area for Questions -->
        <ScrollArea class="flex-1">
          <div class="p-2 pr-3 space-y-4">
            <!-- Question Card -->
            <QuestionCard
              v-for="question in questions.slice()"
              :key="question.id"
              :question="question"
            />
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
  /* top: 0;
  left: 0;
  right: 0;
  bottom: 0; */
}
</style>
