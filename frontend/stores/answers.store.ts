import { defineStore } from "pinia";
import { ref } from "vue";
import type { UUID } from "crypto";
import type { AnswerDetail, AnswerUpdate } from "@/types/api";
import { useAnswer } from "@/composables/useAnswer";

export const useAnswersStore = defineStore("answer", () => {
  // State
  const answers = ref<AnswerDetail[]>([]);
  const currentAnswer = ref<AnswerDetail | null>(null); // Use this for showing the configuration of a single answer in sidebar or anything (Score/Comments modals) that opens from the answer
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const answerApi = useAnswer();

  // Actions
  const fetchAnswersForQuestion = async (questionId: UUID) => {
    isLoading.value = true;
    error.value = null;

    const response = await answerApi.getAnswersForQuestion(questionId);

    if (response.error) {
      error.value = response.error.message;
    } else {
      answers.value = response.data || [];
    }

    isLoading.value = false;
  };

  const fetchAnswersForConfiguration = async (configurationId: UUID) => {
    isLoading.value = true;
    error.value = null;

    const response = await answerApi.getAnswersForConfiguration(configurationId);

    if (response.error) {
      error.value = response.error.message;
    } else {
      answers.value = response.data || [];
    }

    isLoading.value = false;
  };

  const updateAnswerScore = async (questionId: UUID, answerId: UUID, scoreData: AnswerUpdate) => {
    isLoading.value = true;
    error.value = null;

    const response = await answerApi.updateAnswerScore(questionId, answerId, scoreData);

    if (response.error) {
      error.value = response.error.message;
    } else {
      const updatedAnswer = response.data as AnswerDetail;
      const index = answers.value.findIndex((a) => a.id === answerId);
      if (index !== -1) {
        answers.value[index] = updatedAnswer;
      }
      if (currentAnswer.value?.id === answerId) {
        currentAnswer.value = updatedAnswer;
      }
    }

    isLoading.value = false;
  };

  return {
    // State
    answers,
    currentAnswer,
    isLoading,
    error,
    // Actions
    fetchAnswersForQuestion,
    fetchAnswersForConfiguration,
    updateAnswerScore
  };
});
