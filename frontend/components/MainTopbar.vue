<script setup lang="ts">
import { useAttrs } from "vue";
import { useQuestionsModalStore, useSidebarToggleStore } from "@/stores/toggleOpen.store";
import { Button } from "@/components/ui/button";
import { Plus, PanelRightClose, PanelLeftClose } from "lucide-vue-next";
import { useRoute } from "vue-router";

const attrs = useAttrs(); // Access non-prop attributes like `class`

// Accessing Pinia stores
const questionsModalStore = useQuestionsModalStore();
const sidebarToggleStore = useSidebarToggleStore();

// Toggle the sidebar state
const toggleSidebar = () => {
  return sidebarToggleStore.isOpen ? sidebarToggleStore.close() : sidebarToggleStore.open();
};

// Open the modal when "Add Questions" is clicked
const toggleModal = () => {
  questionsModalStore.open();
};

// Get the current route
const route = useRoute();

// Computed property to check if the route ends with '/evaluation'
const showNavigationButtons = computed(() => route.path.endsWith("/evaluation"));
</script>

<template>
  <div v-bind="attrs" class="p-2 mx-2 flex justify-between items-center select-none">
    <!-- App title -->
    <h1 class="text-2xl font-bold text-gray-300">LangChain Evaluator</h1>

    <!-- Navigation Buttons on the Right Side -->
    <div v-if="showNavigationButtons" class="flex items-center space-x-2">
      <!-- Add Questions Button -->
      <Button
        size="xs"
        variant="ghost"
        class="text-sm [text-shadow:_0_1px_1px_rgb(0_0_0_/_10%)] text-gray-300 hover:glassmorphism hover:border-none"
        aria-label="Add Questions"
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
        @click="toggleSidebar"
      >
        <PanelRightClose v-if="sidebarToggleStore.isOpen" :size="22" />
        <PanelLeftClose v-else :size="22" />
      </Button>
    </div>
  </div>

  <!-- Modal for adding questions -->
  <AddQuestionsModal />
</template>
