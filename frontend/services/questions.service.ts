import { BaseService } from "./base.service";
import type { IQuestion } from "@/interfaces/EvaluationSession.interface";
// TODO: Replace with actual data from server
import { questionsData } from "@/assets/testdata/questionData"; // Mock data

export default class QuestionsService extends BaseService {
  private questions: IQuestion[] = questionsData;
  public isProcessing = false;

  /**
   * Adds a new QA pair (Questions + Expected Answers) to the existing list of questions.
   * @param newQuestions - Array of new question data.
   */
  async addQAPair(
    newQuestions: { text: string; expectedAnswers?: string; important: boolean }[]
  ): Promise<void> {
    try {
      // TODO: Replace with actual API call
      // Calculate the last question's ID, defaulting to 0 if there are no questions
      const lastId = this.questions.length > 0 ? this.questions[this.questions.length - 1].id : 0;

      // Map the new questions to include incrementing IDs and empty answers array
      const newQuestionsWithIds = newQuestions.map((q, index) => ({
        id: lastId + index + 1,
        ...q,
        answers: []
      }));

      this.questions.push(...newQuestionsWithIds);
    } catch (error) {
      this.handleError(error, "QuestionsService.addQAPair()");
    }
  }

  /**
   * Retrieves all questions.
   * @returns Array of questions.
   */
  async getQuestions(): Promise<IQuestion[]> {
    try {
      // TODO: Replace with actual API call
      return this.questions;
    } catch (error) {
      this.handleError(error, "QuestionsService.getQuestions()");
      return [];
    }
  }

  /**
   * Simulates the file upload process by processing the file and adding a new question.
   * Sets isProcessing to true while processing the file.
   * @param file - The file to be uploaded.
   * @returns void
   * @throws Error if there is an issue uploading the file
   */
  async handleFileUpload(file: File): Promise<void> {
    this.isProcessing = true;
    try {
      // Replace with actual file upload logic
      await this.delay(1000);
      const newQuestion: IQuestion = {
        id: this.questions.length + 1,
        text: `New question from ${file.name}`,
        important: false,
        answers: []
      };
      this.questions.push(newQuestion);
    } catch (error) {
      this.handleError(error, "handleFileUpload");
    } finally {
      this.isProcessing = false;
    }
  }
}
