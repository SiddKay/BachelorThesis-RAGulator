<script lang="ts" setup>
import { useQuestionsStore } from "@/stores/questionsStore";
import { storeToRefs } from "pinia";

const questionsStore = useQuestionsStore();
const { questions } = storeToRefs(questionsStore);
</script>

<template>
  <main class="relative w-screen h-screen bg-neutral-950 flex items-center justify-center">
    <!-- Morphing Gradient as background -->
    <MorphingGradient class="absolute inset-0 z-0" />

    <!-- Question Card with Answers -->
    <QuestionCard :question="questions[0]" />
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
</style>
