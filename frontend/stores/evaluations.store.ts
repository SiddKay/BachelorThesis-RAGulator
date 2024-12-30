import { ref } from "vue";
import { defineStore } from "pinia";
import type { IChain, IConfiguration, IQuestion, IAnswer } from "~/types/models";
import { useChain } from "@/composables/api/useChain";

export const useEvaluationStore = defineStore("evaluation", () => {
  // State
  const availableChains = ref<string[]>([]);
  const selectedChains = ref<IChain[]>([]);
  const questions = ref<IQuestion[]>([]);
  const currentConfig = ref<IConfiguration | null>(null);
  const answers = ref<IAnswer[]>([]);

  // Actions
  const fetchAvailableChains = async () => {
    const { data, error } = await useChain().getAvailableChains();

    if (error.value) {
      throw createError({
        statusCode: error.value.statusCode,
        message: "Failed to fetch chains"
      });
    }

    availableChains.value = data.value || [];
  };

  const selectChains = async (sessionId: string, fileNames: string[]) => {
    const { data, error } = await useChain().selectChains(sessionId, fileNames);

    if (error.value) {
      throw createError({
        statusCode: error.value.statusCode,
        message: "Failed to select chains"
      });
    }

    selectedChains.value = data.value || [];
  };

  // Return store properties and methods
  return {
    availableChains,
    selectedChains,
    questions,
    currentConfig,
    answers,
    fetchAvailableChains,
    selectChains
  };
});
