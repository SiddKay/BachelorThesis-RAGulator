<script setup lang="ts">
import { useAttrs } from "vue";
import { useQuestionsModalStore, useSidebarToggleStore } from "@/stores/toggleOpen.store";
import { useSessionStore } from "@/stores/sessions.store";
import { Button } from "@/components/ui/button";
import { Plus, PanelRightClose, PanelLeftClose } from "lucide-vue-next";
import { useRoute } from "vue-router";

const attrs = useAttrs();
const route = useRoute();

// Accessing Pinia stores
const sessionStore = useSessionStore();
const questionsModalStore = useQuestionsModalStore();
const sidebarToggleStore = useSidebarToggleStore();

// Toggle handlers
const toggleSidebar = () => {
  return sidebarToggleStore.isOpen ? sidebarToggleStore.close() : sidebarToggleStore.open();
};

const toggleModal = () => {
  questionsModalStore.open();
};

// Dynamic content logic
const isEvaluationScreen = computed(() => route.path.endsWith("/evaluation"));
const isSessionsScreen = computed(() => route.path === "/sessions");

const screenTitle = computed(() => {
  if (isSessionsScreen.value) return "Sessions";
  if (isEvaluationScreen.value) {
    return sessionStore.currentSession?.name || "Evaluation";
  }
  return "";
});
</script>

<template>
  <div v-bind="attrs" class="p-2 mx-2 flex justify-between items-center select-none">
    <!-- Left: App title (static) -->
    <div class="flex-col w-1/3">
      <h1 class="text-2xl font-bold text-gray-300">RAGulator</h1>
      <h3 class="text-base font-semibold text-gray-400">LangChain Evaluator</h3>
    </div>

    <!-- Center: Screen Title -->
    <div class="flex-1 text-center">
      <h2 class="text-xl font-semibold text-gray-300">{{ screenTitle }}</h2>
    </div>

    <!-- Right: Navigation Buttons -->
    <div class="w-1/3 flex justify-end">
      <div v-if="isEvaluationScreen" class="flex items-center space-x-2">
        <!-- Add Questions Button -->
        <Button
          size="xs"
          variant="ghost"
          class="text-sm [text-shadow:_0_1px_1px_rgb(0_0_0_/_10%)] text-gray-300 hover:glassmorphism hover:border-none"
          aria-label="Add Questions"
          title="Add Questions"
          @click="toggleModal"
        >
          <Plus class="mr-2 h-4 w-4" />Add Questions
        </Button>

        <!-- Toggle Sidebar Button -->
        <Button
          size="sm"
          variant="link"
          class="p-0 text-gray-300 hover:text-gray-50"
          aria-label="Open/close Sidebar"
          :title="sidebarToggleStore.isOpen ? 'Close' : 'Open'"
          @click="toggleSidebar"
        >
          <PanelRightClose v-if="sidebarToggleStore.isOpen" :size="22" />
          <PanelLeftClose v-else :size="22" />
        </Button>
      </div>

      <!-- TODO: Add functionality to open "Add Sessions" modal -->
    </div>
  </div>

  <!-- Modal for adding questions -->
  <AddQuestionsModal />
</template>
