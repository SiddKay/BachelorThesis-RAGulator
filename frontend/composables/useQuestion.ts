import type { UUID } from "crypto";
import { useApi } from "@/composables/useApi";
import type { Question, QuestionDetail, QuestionCreate } from "@/types/api";

export const useQuestion = () => {
  const api = useApi();

  const getQuestions = (sessionId: UUID) =>
    api.get<QuestionDetail[]>(`/sessions/${sessionId}/questions`);

  const createQuestion = (sessionId: UUID, data: QuestionCreate) =>
    api.post<Question>(`/sessions/${sessionId}/questions`, data);

  const createQuestionsBulk = (sessionId: UUID, questions: QuestionCreate[]) =>
    api.post<Question[]>(`/sessions/${sessionId}/questions/bulk`, { questions });

  const updateQuestion = (sessionId: UUID, questionId: UUID, data: Partial<QuestionCreate>) =>
    api.patch<QuestionDetail>(`/sessions/${sessionId}/questions/${questionId}`, data);

  const deleteQuestion = (sessionId: UUID, questionId: UUID) =>
    api.delete<Question>(`/sessions/${sessionId}/questions/${questionId}`);

  const deleteQuestionsBulk = (sessionId: UUID, questionIds: UUID[]) =>
    api.delete<Question[]>(`/sessions/${sessionId}/questions/bulk`, { question_ids: questionIds });

  const deleteAllQuestions = (sessionId: UUID) =>
    api.delete<Question[]>(`/sessions/${sessionId}/questions`);

  return {
    createQuestion,
    createQuestionsBulk,
    getQuestions,
    updateQuestion,
    deleteQuestion,
    deleteQuestionsBulk,
    deleteAllQuestions
  };
};
