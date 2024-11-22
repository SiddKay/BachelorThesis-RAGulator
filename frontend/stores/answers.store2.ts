import { defineStore } from "pinia";
import AnswersService from "@/services/answers.service";
import { useQuestionsStore } from "./questions.store2";
import type { IAnswer } from "~/types/models2";

const answersService = new AnswersService();

export const useAnswersStore = defineStore("answers", () => {
  const questionsStore = useQuestionsStore();
  const selectedAnswer = ref<IAnswer | null>(null);
  const isProcessing = ref(false);

  /**
   * Generates an answer for the specified question.
   *
   * @param questionId - The ID of the question for which to generate an answer.
   * @param chainId - The ID of the chain for which to generate an answer.
   * @param configId - The ID of the configuration for which to generate an answer.
   * @returns The generated answer.
   */
  const generateAnswer = async (questionId: string, chainId: string, configId: string) => {
    isProcessing.value = true;
    try {
      const answer = await answersService.generateAnswer(questionId, chainId, configId);
      return answer;
    } finally {
      isProcessing.value = false;
    }
  };

  /**
   * Selects an answer by its question ID and configVersion.
   * This is is used to record the selected answer for further processing (e.g., scoring, commenting).
   *
   * @param questionId - The ID of the question.
   * @param configVersion - The configuration version of the answer.
   * @returns void
   */
  const selectAnswer = async (questionId: string, configVersion: string) => {
    const question = questionsStore.questions.find((q) => q.question_text === questionId);
    selectedAnswer.value = question
      ? await answersService.findAnswer(question, configVersion)
      : null;
  };

  /**
   * Clears the selected answer after processing (e.g., scoring, commenting).
   * @returns void
   */
  const clearSelectedAnswer = () => {
    selectedAnswer.value = null;
  };

  return {
    isProcessing,
    generateAnswer,
    selectedAnswer,
    selectAnswer,
    clearSelectedAnswer
  };
});
