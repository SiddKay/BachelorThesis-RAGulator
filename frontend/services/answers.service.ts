import type { IAnswer } from "~/types/models2";
import { BaseService } from "./base.service";

export default class AnswersService extends BaseService {
  // /**
  //  * Finds an answer in the specified question based on config version.
  //  * @param question - The question containing answers.
  //  * @param configVersion - The configuration version of the answer.
  //  */
  // async findAnswer(question: IQuestion, configId: string): Promise<IAnswer | null> {
  //   try {
  //     const answer = question.answers?.find((a) => a.configuration_id === configId) || null;
  //     return answer;
  //   } catch (error) {
  //     this.handleError(error, "findAnswer");
  //     return null;
  //   }
  // }

  /**
   * Updates the score of a specific answer.
   * @param answer - The answer to update.
   * @param score - The new score to assign.
   */
  async updateScore(answer: IAnswer, score: number): Promise<void> {
    try {
      // Replace with actual API call
      answer.score = score;
    } catch (error) {
      this.handleError(error, "updateScore");
    }
  }

  /**
   * Generates an answer for the specified question.
   * @param questionId - The ID of the question for which to generate an answer.
   */
  async generateAnswer(questionId: string, chainId: string, configId: string): Promise<IAnswer> {
    try {
      // TODO: Replace with actual API call
      await this.delay(2000);
      return {
        id: crypto.randomUUID(),
        chain_id: chainId,
        question_id: questionId,
        configuration_id: configId,
        generated_answer: `Generated answer for question ${questionId}`,
        created_at: new Date().toISOString(),
        comments: []
      };
    } catch (error) {
      this.handleError(error, "generateAnswer");
      throw error;
    }
  }
}
