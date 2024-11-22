import type { UUID } from "crypto";
import { useApi } from "@/composables/useApi";
import type { AnswerDetail, AnswerUpdate } from "@/types/api";

export const useAnswer = () => {
  const api = useApi();

  const getAnswersForQuestion = (questionId: UUID) =>
    api.get<AnswerDetail[]>(`/questions/${questionId}/answers`);

  const getAnswersForConfiguration = (configurationId: UUID) =>
    api.get<AnswerDetail[]>(`/configurations/${configurationId}/answers`);

  const updateAnswerScore = (questionId: UUID, answerId: UUID, data: AnswerUpdate) =>
    api.patch<AnswerDetail>(`/questions/${questionId}/answers/${answerId}`, data);

  return {
    getAnswersForQuestion,
    getAnswersForConfiguration,
    updateAnswerScore
  };
};
