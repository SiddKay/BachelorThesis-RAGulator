import { defineStore } from "pinia";
import { ref } from "vue";

// TODO: Replace with actual data from server
import { questionsData } from "@/assets/testdata/questionData";
import type { IQuestion, IAnswer } from "@/interfaces/EvaluationSession.interface";

/**
 * Questions store that manages the state of questions and answers.
 */
export const useQuestionsStore = defineStore("questions", () => {
  // TODO: Replace with json
  const questions = ref<IQuestion[]>(questionsData);

  const selectedAnswer = ref<IAnswer | null>(null);
  const selectedQuestionId = ref<number | null>(null);
  const newComment = ref<string>("");
  const isProcessing = ref(false);

  /**
   * Adds new questions to the existing questions array.
   *
   * @param newQuestions - An array of new questions to be added.
   * @returns void
   * @throws Error if newQuestions is not an array or is empty
   */
  const addQuestions = (newQuestions: { text: string; important: boolean }[]) => {
    try {
      // Validate that newQuestions is an array
      if (!Array.isArray(newQuestions) || newQuestions.length === 0) {
        console.error("Invalid input: newQuestions should be a non-empty array");
        return;
      }

      // Calculate the last question's ID, defaulting to 0 if there are no questions
      const lastId =
        questions.value.length > 0 ? questions.value[questions.value.length - 1].id : 0;

      // Map the new questions to include incrementing IDs and empty answers array
      const newQuestionsWithIds = newQuestions.map((q, index) => ({
        id: lastId + index + 1,
        ...q,
        answers: []
      }));

      // Push the new questions to the existing array
      questions.value.push(...newQuestionsWithIds);
      console.log(`${newQuestions.length} new questions added successfully.`);
    } catch (error) {
      console.error("Error adding questions:", error);
    }
  };

  /**
   * Selects an answer by its question ID and configVersion.
   * This is is used to record the selected answer for further processing (e.g., scoring, commenting).
   *
   * @param questionId - The ID of the question.
   * @param configVersion - The configuration version of the answer.
   * @returns void
   * @throws Error if the question or answer is not found
   */
  const selectAnswer = (questionId: number, configVersion: number) => {
    try {
      const question = questions.value.find((q) => q.id === questionId);

      if (!question) {
        console.error(`Question with ID ${questionId} not found`);
        return;
      }

      const answer = question.answers.find((a) => a.configVersion === configVersion);

      if (!answer) {
        console.error(
          `Answer with version ${configVersion} not found for question ID ${questionId}`
        );
        return;
      }

      selectedAnswer.value = answer;
      selectedQuestionId.value = questionId;
    } catch (error) {
      console.error("Error selecting answer:", error);
    }
  };

  /**
   * Clears the selected answer and resets related states.
   * This is used to clear the selected answer after processing (e.g., scoring, commenting).
   *
   * @returns void
   * @throws Error if there is an issue clearing the selected answer
   */
  const clearSelectedAnswer = () => {
    try {
      selectedAnswer.value = null;
      selectedQuestionId.value = null;
      newComment.value = "";
      console.log("Selected answer and related states have been cleared.");
    } catch (error) {
      console.error("Error clearing selected answer:", error);
    }
  };

  // TODO: put these methods in a separate annotations store
  /**
   * Updates the score of an answer by its question ID and configVersion.
   * @param questionId - The ID of the question.
   * @param configVersion - The configuration version of the answer.
   * @param score - The new score to be set.
   * @returns void
   * @throws Error if the question or answer is not found
   */
  const updateScore = (questionId: number, configVersion: number, score: number) => {
    try {
      const question = questions.value.find((q) => q.id === questionId);
      if (!question) {
        console.error(`Question with ID ${questionId} not found`);
        return;
      }

      const answer = question.answers.find((a) => a.configVersion === configVersion);
      if (!answer) {
        console.error(
          `Answer with configVersion ${configVersion} not found for question ID ${questionId}`
        );
        return;
      }

      answer.score = score;
      console.log(
        `Score updated successfully for answer with configVersion ${configVersion} of question ID ${questionId}`
      );
    } catch (error) {
      console.error("Error updating score:", error);
    }
  };

  /**
   * Adds a comment to the selected answer.
   * @returns void
   * @throws Error if there is an issue adding the comment to the selected answer
   */
  const addCommentToSelectedAnswer = () => {
    try {
      if (!selectedAnswer.value) {
        console.error("No answer selected");
        return;
      }

      const comment = newComment.value.trim();
      if (comment === "") {
        console.error("Comment cannot be empty");
        return;
      }

      if (!Array.isArray(selectedAnswer.value.comments)) {
        selectedAnswer.value.comments = [];
      }

      selectedAnswer.value.comments.push(comment);
      newComment.value = "";
      console.log("Comment added successfully to the selected answer.");
    } catch (error) {
      console.error("Error adding comment to selected answer:", error);
    }
  };

  /**
   * Deletes a comment from the selected answer.
   * @param commentIndex - The index of the comment to be deleted.
   * @returns void
   * @throws Error if there is an issue deleting the comment from the selected answer
   */
  const deleteCommentFromSelectedAnswer = (commentIndex: number) => {
    try {
      if (!selectedAnswer.value) {
        console.error("No answer selected");
        return;
      }

      if (
        !selectedAnswer.value.comments ||
        commentIndex < 0 ||
        commentIndex >= selectedAnswer.value.comments.length
      ) {
        console.error("Invalid comment index");
        return;
      }

      selectedAnswer.value.comments.splice(commentIndex, 1);
      console.log("Comment deleted successfully from the selected answer.");
    } catch (error) {
      console.error("Error deleting comment from selected answer:", error);
    }
  };

  // TODO: Implement the actual runChain method
  /**
   * Simulates running an LCEL chain with a delay.
   *
   * @returns void
   * @throws Error if there is an issue running the chain
   */
  const runChain = async () => {
    isProcessing.value = true;
    try {
      // Simulating an API call
      await new Promise((resolve) => setTimeout(resolve, 2000));
      questions.value = questions.value.map((q) => ({
        ...q,
        answers: [
          ...q.answers,
          {
            id: q.answers.length + 1,
            questionId: q.id,
            configVersion: q.answers.length + 1,
            text: `New answer for: ${q.text}`,
            comments: [],
            score: 0
          }
        ]
      }));
    } catch (error) {
      console.error("Error running chain:", error);
    } finally {
      isProcessing.value = false;
    }
  };

  /**
   * Simulates the file upload process by processing the file and adding a new question.
   * Sets isProcessing to true while processing the file.
   * @param file - The file to be uploaded.
   * @returns void
   * @throws Error if there is an issue uploading the file
   */
  const handleFileUpload = async (file: File) => {
    isProcessing.value = true;
    try {
      // Process the file (simulated)
      await new Promise((resolve) => setTimeout(resolve, 1000));
      const newQuestion: IQuestion = {
        id: questions.value.length + 1,
        text: `New question from ${file.name}`,
        important: false,
        answers: []
      };
      questions.value.push(newQuestion);
    } catch (error) {
      console.error("Error uploading file:", error);
    } finally {
      isProcessing.value = false;
    }
  };

  return {
    questions,
    isProcessing,
    addQuestions,
    selectAnswer,
    clearSelectedAnswer,
    updateScore,
    addCommentToSelectedAnswer,
    deleteCommentFromSelectedAnswer,
    runChain,
    handleFileUpload
  };
});
