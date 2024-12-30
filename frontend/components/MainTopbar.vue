<script setup lang="ts">
import { useAttrs, ref, onUnmounted } from "vue";
import {
  useQuestionsModalStore,
  useSidebarToggleStore,
  useMorphingGradientBgToggleStore,
  useCreateSessionModalStore
} from "@/stores/toggleOpen.store";
import { useSessionStore } from "@/stores/sessions.store";
import { Button } from "@/components/ui/button";
import { Plus, PanelRightClose, PanelLeftClose } from "lucide-vue-next";
import { useRoute, useRouter } from "vue-router";
const attrs = useAttrs();
const route = useRoute();
const router = useRouter();

// Accessing Pinia stores
const sessionStore = useSessionStore();
const questionsModalStore = useQuestionsModalStore();
const sidebarToggleStore = useSidebarToggleStore();
const morphingGradientBgToggleStore = useMorphingGradientBgToggleStore();
const createSessionModalStore = useCreateSessionModalStore();

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

const handleH1Click = () => {
  if (!isSessionsScreen.value) {
    router.push("/sessions");
  }
};

// Fancy title click logic
const colors = [
  "text-green-200",
  "text-cyan-200",
  "text-red-200",
  "text-yellow-200",
  "text-pink-200",
  "text-purple-200",
  "text-blue-200"
];

// Click counter logic
const clickCount = ref(0);
const lastClickTime = ref(0);
const colorIndex = ref(0);

const handleH3Click = () => {
  // Don't process clicks if gradient is already open
  if (morphingGradientBgToggleStore.isOpen) return;

  const now = Date.now();
  if (now - lastClickTime.value > 1000) {
    // Reset if more than 1 second between clicks
    clickCount.value = 1;
  } else {
    clickCount.value++;
  }
  lastClickTime.value = now;

  // Cycle through colors
  colorIndex.value = (colorIndex.value + 1) % colors.length;

  // Clear any existing timeout
  if (colorResetTimeout.value) clearTimeout(colorResetTimeout.value);

  // Set new timeout to reset color after 1 second
  colorResetTimeout.value = setTimeout(() => {
    if (!morphingGradientBgToggleStore.isOpen) {
      clickCount.value = 0;
      colorIndex.value = 0;
    }
  }, 1000);

  if (clickCount.value === 5) {
    morphingGradientBgToggleStore.open();
    clickCount.value = 0;
    colorIndex.value = 0; // Reset color
  }
};

// Cleanup
const colorResetTimeout = ref<NodeJS.Timeout | null>(null);
onUnmounted(() => {
  if (colorResetTimeout.value) {
    clearTimeout(colorResetTimeout.value);
  }
});
</script>

<template>
  <div v-bind="attrs" class="p-2 mx-2 flex justify-between items-center select-none">
    <!-- Left: App title (static) -->
    <div class="flex-col w-1/3">
      <h1
        :class="[
          'w-fit text-2xl font-bold transition-colors duration-100',
          !isSessionsScreen ? 'text-gray-400 cursor-pointer hover:text-gray-50' : 'text-gray-50'
        ]"
        :title="!isSessionsScreen ? 'Back to Sessions List' : undefined"
        @click="handleH1Click"
      >
        RAGulator
      </h1>
      <h3
        :class="[
          'w-fit text-base font-semibold transition-colors duration-150',
          clickCount === 0 ? 'text-gray-500' : colors[colorIndex]
        ]"
        @click="handleH3Click"
      >
        LangChain Evaluator
      </h3>
    </div>

    <!-- Center: Screen Title -->
    <div class="flex-1 text-center">
      <h2 class="text-xl font-semibold text-gray-300">{{ screenTitle }}</h2>
    </div>

    <!-- Right: Navigation Buttons -->
    <div class="w-1/3 flex justify-end">
      <!-- Toggle MorphingGradient BG -->
      <Button
        v-if="morphingGradientBgToggleStore.isOpen"
        size="xs"
        variant="ghost"
        class="text-sm [text-shadow:_0_1px_1px_rgb(0_0_0_/_10%)] text-gray-300 hover:glassmorphism hover:border-none"
        aria-label="dark-mode"
        title="Dark mode"
        @click="morphingGradientBgToggleStore.toggle()"
      >
        <span v-if="morphingGradientBgToggleStore.isOpen">Dark Theme</span>
      </Button>

      <!-- Case: Sessions Screen -->
      <div v-if="isSessionsScreen" class="flex items-center space-x-2">
        <Button
          size="xs"
          variant="ghost"
          class="text-sm [text-shadow:_0_1px_1px_rgb(0_0_0_/_10%)] text-gray-300 hover:glassmorphism hover:border-none"
          aria-label="Create Session"
          title="Create Session"
          @click="createSessionModalStore.open"
        >
          <Plus class="mr-2 h-4 w-4" />New Session
        </Button>
      </div>

      <!-- Case: Evaluations Screen -->
      <div v-else-if="isEvaluationScreen" class="flex items-center space-x-2">
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
    </div>
  </div>

  <!-- Modal for adding questions -->
  <AddQuestionsModal />
  <CreateSessionModal />
</template>
