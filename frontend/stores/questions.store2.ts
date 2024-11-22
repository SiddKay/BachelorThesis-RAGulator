import { defineStore } from "pinia";
import { ref } from "vue";
import QuestionsService from "~/services/questions.service";
import type { IQuestion } from "~/types/models2";

const questionsService = new QuestionsService();

/**
 * Questions store that manages the state of questions and answers.
 */
export const useQuestionsStore = defineStore("questions", () => {
  const questions = ref<IQuestion[]>([]);
  const isProcessing = ref(false);

  /**
   * Fetches questions from the API via the service and updates the store.
   * @returns void
   * @throws Error if there is an issue fetching the questions
   */
  const fetchQuestions = async () => {
    isProcessing.value = true;
    try {
      questions.value = await questionsService.getQuestions();
    } finally {
      isProcessing.value = false;
    }
  };

  /**
   * Adds new questions locally to the store.
   * @param newQuestions - The new questions to be added.
   * @returns void
   * @throws Error if there is an issue adding the questions
   */
  const addQAPair = async (newQuestions: { question_text: string; expectedAnswers?: string }[]) => {
    isProcessing.value = true;
    try {
      await questionsService.addQAPair(newQuestions);
      questions.value = await questionsService.getQuestions(); // Refresh state
    } finally {
      isProcessing.value = false;
    }
  };

  const handleFileUpload = async (file: File) => {
    isProcessing.value = true;
    try {
      await questionsService.handleFileUpload(file);
      questions.value = await questionsService.getQuestions(); // Refresh state
    } finally {
      isProcessing.value = false;
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
  const updateScore = (questionId: string, configId: string, score: number) => {
    try {
      const question = questions.value.find((q) => q.question_text === questionId);
      if (!question) {
        console.error(`Question with ID ${questionId} not found`);
        return;
      }

      const answer = question.answers?.find((a) => a.configuration_id === configId);
      if (!answer) {
        console.error(
          `Answer with configVersion ${configId} not found for question ID ${questionId}`
        );
        return;
      }

      answer.score = score;
      console.log(
        `Score updated successfully for answer with configVersion ${configId} of question ID ${questionId}`
      );
    } catch (error) {
      console.error("Error updating score:", error);
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
          ...(q.answers ?? []),
          {
            id: crypto.randomUUID(),
            chain_id: "chain_id_placeholder",
            question_id: "abc",
            configuration_id: "config_id_placeholder",
            generated_answer: `New answer for: ${q.question_text}`,
            created_at: new Date().toISOString(),
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

  return {
    questions,
    isProcessing,
    fetchQuestions,
    addQAPair,
    handleFileUpload,
    updateScore,
    runChain
  };
});
