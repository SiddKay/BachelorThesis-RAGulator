<script setup lang="ts">
import { useQuestionsModalStore, useSidebarToggleStore } from "@/stores/toggleOpenStore";
import { Button } from "@/components/ui/button";
import { Plus, PanelRightClose, PanelLeftClose } from "lucide-vue-next";

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
</script>

<template>
  <div class="p-2 flex justify-between items-center select-none">
    <!-- App title -->
    <h1 class="text-2xl font-bold text-gray-300">LangChain Evaluator</h1>

    <!-- Navigation Buttons on the Right Side -->
    <div class="flex items-center space-x-2">
      <!-- Add Questions Button -->
      <Button
        size="xs"
        variant="ghost"
        class="text-sm [text-shadow:_0_1px_1px_rgb(0_0_0_/_10%)] hover:glassmorphism hover:border-none"
        @click="toggleModal"
      >
        <Plus class="mr-2 h-4 w-4" />Add Questions
      </Button>

      <!-- Toggle Sidebar Button -->
      <Button size="sm" variant="link" class="p-0" @click="toggleSidebar">
        <PanelRightClose
          v-if="sidebarToggleStore.isOpen"
          :size="22"
          class="text-gray-300 hover:text-gray-50"
        />
        <PanelLeftClose v-else :size="22" class="text-gray-300 hover:text-gray-50" />
      </Button>
    </div>
  </div>

  <!-- Modal for adding questions -->
  <AddQuestionsModal />
</template>
