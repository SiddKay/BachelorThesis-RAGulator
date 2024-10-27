import { defineStore } from "pinia";
import AnswersService from "@/services/answers.service";
import { useQuestionsStore } from "./questions.store";
import type { IAnswer } from "@/interfaces/EvaluationSession.interface";

const answersService = new AnswersService();

export const useAnswersStore = defineStore("answers", () => {
  const questionsStore = useQuestionsStore();
  const selectedAnswer = ref<IAnswer | null>(null);
  const isProcessing = ref(false);

  /**
   * Generates an answer for the specified question.
   *
   * @param questionId - The ID of the question for which to generate an answer.
   * @returns The generated answer.
   */
  const generateAnswer = async (questionId: number) => {
    isProcessing.value = true;
    try {
      const answer = await answersService.generateAnswer(questionId);
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
  const selectAnswer = async (questionId: number, configVersion: number) => {
    const question = questionsStore.questions.find((q) => q.id === questionId);
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
