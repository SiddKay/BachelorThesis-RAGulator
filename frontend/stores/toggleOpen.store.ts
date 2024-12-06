import { defineStore } from "pinia";
import { ref } from "vue";

function createToggleStore(storeId: string) {
  return defineStore(storeId, () => {
    const isOpen = ref(false);

    // Function to open the component
    function open() {
      isOpen.value = true;
    }

    // Function to close the component
    function close() {
      isOpen.value = false;
    }

    function toggle() {
      isOpen.value = !isOpen.value;
    }

    return {
      isOpen,
      open,
      close,
      toggle
    };
  });
}

export const useQuestionsModalStore = createToggleStore("questionsModal");
export const useAnnotationsModalStore = createToggleStore("annotationsModal");
export const useSidebarToggleStore = createToggleStore("sidebarToggle");
export const useMorphingGradientBgToggleStore = createToggleStore("morphingGradientBgToggle");
