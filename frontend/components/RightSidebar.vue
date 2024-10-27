<script setup lang="ts">
/**----------------------------- Imports ----------------------------------- */
import { storeToRefs } from "pinia";
import { useConfigStore } from "@/stores/chainConfig.store";
import { useQuestionsStore } from "@/stores/questions.store";
import { useSidebarToggleStore } from "@/stores/toggleOpen.store";

import Slider from "./ui/slider/Slider.vue";
import Textarea from "./ui/textarea/Textarea.vue";
import Button from "./ui/button/Button.vue";
import { Loader2 } from "lucide-vue-next";

/**----------------------------- Methods ----------------------------------- */

// Accessing Pinia stores
const questionsStore = useQuestionsStore();
const configStore = useConfigStore();
const sidebarToggleStore = useSidebarToggleStore();

const { isProcessing } = storeToRefs(questionsStore);
const { isOpen: isSidebarOpen } = storeToRefs(sidebarToggleStore);
const { parameter1, parameter2, prompt } = storeToRefs(configStore);
</script>

<template>
  <aside
    v-if="isSidebarOpen"
    class="m-2 ml-1 rounded-lg glassmorphism transition-all duration-300 ease-in-out overflow-hidden w-64"
  >
    <div class="p-2 pt-3 shadow flex justify-between items-center select-none">
      <h2 class="text-lg font-semibold text-gray-300">Chain Config</h2>
    </div>
    <div class="p-4 space-y-4">
      <div>
        <label class="pb-3 block text-sm font-medium text-gray-300">Parameter 1</label>
        <Slider v-model="parameter1" :min="0" :max="100" :step="1" />
      </div>
      <div>
        <label class="pb-3 block text-sm font-medium text-gray-300">Parameter 2</label>
        <Slider v-model="parameter2" :min="0" :max="100" :step="1" />
      </div>
      <div>
        <label class="pb-3 block text-sm font-medium text-gray-300">Prompt</label>
        <Textarea v-model="prompt" placeholder="Enter your prompt here..." />
      </div>
      <Button
        variant="ghost"
        class="w-full text-sm [text-shadow:_0_1px_1px_rgb(0_0_0_/_10%)] glassmorphism border-none"
        :disabled="isProcessing"
        aria-label="Run Chain"
        @click="questionsStore.runChain"
      >
        <Loader2 v-if="isProcessing" class="mr-2 h-4 w-4 animate-spin" />
        <span v-else>Run Chain</span>
      </Button>
    </div>
  </aside>
</template>
