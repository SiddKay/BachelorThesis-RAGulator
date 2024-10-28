import { defineStore } from "pinia";
import AnnotationsService from "@/services/annotations.service";
import { useAnswersStore } from "./answers.store";

const annotationsService = new AnnotationsService();

export const useAnnotationsStore = defineStore("annotations", () => {
  const answersStore = useAnswersStore();
  const isProcessing = ref(false);

  /**
   * Adds a new comment to the selected answer.
   * @param newComment - The new comment to be added.
   * @returns void
   */
  const addComment = async (newComment: string) => {
    if (!newComment.trim()) return;

    isProcessing.value = true;

    try {
      if (answersStore.selectedAnswer) {
        await annotationsService.addComment(answersStore.selectedAnswer, newComment);
      }
    } finally {
      isProcessing.value = false;
    }
  };

  /**
   * Deletes a comment from the selected answer.
   * @param commentIndex - The index of the comment to be deleted.
   * @returns void
   */
  const deleteComment = async (commentIndex: number) => {
    isProcessing.value = true;
    try {
      if (answersStore.selectedAnswer) {
        await annotationsService.deleteComment(answersStore.selectedAnswer, commentIndex);
      }
    } finally {
      isProcessing.value = false;
    }
  };

  return {
    isProcessing,
    addComment,
    deleteComment
  };
});
