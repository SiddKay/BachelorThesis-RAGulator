import { defineStore } from "pinia";
import { ref } from "vue";
import type { UUID } from "crypto";
import type { Question, QuestionDetail, QuestionCreate } from "@/types/api";
import { useQuestion } from "@/composables/useQuestion";

export const useQuestionsStore = defineStore("question", () => {
  // State
  const basicQuestions = ref<QuestionDetail[]>([]);
  const questionDetails = ref<QuestionDetail[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const questionApi = useQuestion();

  // Computed
  const allQuestions = computed<QuestionDetail[]>(() => {
    return [...questionDetails.value, ...basicQuestions.value];
  });

  // Actions
  const fetchQuestions = async (sessionId: UUID) => {
    isLoading.value = true;
    error.value = null;

    const response = await questionApi.getQuestions(sessionId);

    if (response.error) {
      error.value = response.error.message;
    } else {
      questionDetails.value = response.data || [];
      // Clear basic questions when loading details
      basicQuestions.value = [];
    }

    isLoading.value = false;
  };

  const createQuestion = async (sessionId: UUID, questionData: QuestionCreate) => {
    isLoading.value = true;
    error.value = null;

    const response = await questionApi.createQuestion(sessionId, questionData);

    if (response.error) {
      error.value = response.error.message;
    } else {
      basicQuestions.value.push({
        ...(response.data as Question),
        answers: []
      });
    }

    isLoading.value = false;
  };

  const createQuestionsBulk = async (sessionId: UUID, questionsData: QuestionCreate[]) => {
    isLoading.value = true;
    error.value = null;

    const response = await questionApi.createQuestionsBulk(sessionId, questionsData);

    if (response.error) {
      error.value = response.error.message;
    } else {
      const newQuestions = (response.data as Question[]).map((q) => ({
        ...q,
        answers: []
      }));
      basicQuestions.value = [...basicQuestions.value, ...newQuestions];
    }

    isLoading.value = false;
  };

  const updateQuestion = async (
    sessionId: UUID,
    questionId: UUID,
    questionData: Partial<QuestionCreate>
  ) => {
    isLoading.value = true;
    error.value = null;

    const response = await questionApi.updateQuestion(sessionId, questionId, questionData);

    if (response.error) {
      error.value = response.error.message;
    } else {
      const updatedQuestion = response.data as QuestionDetail;
      const index = questionDetails.value.findIndex((q) => q.id === questionId);
      if (index !== -1) {
        questionDetails.value[index] = updatedQuestion;
      }
    }

    isLoading.value = false;
  };

  const deleteQuestion = async (sessionId: UUID, questionId: UUID) => {
    isLoading.value = true;
    error.value = null;

    const response = await questionApi.deleteQuestion(sessionId, questionId);

    if (response.error) {
      error.value = response.error.message;
    } else {
      basicQuestions.value = basicQuestions.value.filter((q) => q.id !== questionId);
      questionDetails.value = questionDetails.value.filter((q) => q.id !== questionId);
    }

    isLoading.value = false;
  };

  const deleteQuestionsBulk = async (sessionId: UUID, questionIds: UUID[]) => {
    isLoading.value = true;
    error.value = null;

    const response = await questionApi.deleteQuestionsBulk(sessionId, questionIds);

    if (response.error) {
      error.value = response.error.message;
    } else {
      basicQuestions.value = basicQuestions.value.filter((q) => !questionIds.includes(q.id));
      questionDetails.value = questionDetails.value.filter((q) => !questionIds.includes(q.id));
    }

    isLoading.value = false;
  };

  const deleteAllQuestions = async (sessionId: UUID) => {
    isLoading.value = true;
    error.value = null;

    const response = await questionApi.deleteAllQuestions(sessionId);

    if (response.error) {
      error.value = response.error.message;
    } else {
      basicQuestions.value = [];
      questionDetails.value = [];
    }

    isLoading.value = false;
  };

  return {
    // State
    allQuestions,
    basicQuestions,
    questionDetails,
    isLoading,
    error,
    // Actions
    fetchQuestions,
    createQuestion,
    createQuestionsBulk,
    updateQuestion,
    deleteQuestion,
    deleteQuestionsBulk,
    deleteAllQuestions
  };
});
