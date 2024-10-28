import type { IAnswer } from "@/interfaces/EvaluationSession.interface";
import { BaseService } from "./base.service";

export default class AnnotationsService extends BaseService {
  /**
   * Adds a comment to a specified answer.
   * @param answer - The answer to which the comment is added.
   * @param comment - The comment to add.
   */
  async addComment(answer: IAnswer, comment: string): Promise<void> {
    try {
      if (!Array.isArray(answer.comments)) {
        answer.comments = [];
      }
      answer.comments.push(comment);
    } catch (error) {
      this.handleError(error, "addComment");
    }
  }

  /**
   * Deletes a comment from a specified answer.
   * @param answer - The answer from which the comment is removed.
   * @param index - The index of the comment to delete.
   */
  async deleteComment(answer: IAnswer, index: number): Promise<void> {
    try {
      if (Array.isArray(answer.comments) && index >= 0 && index < answer.comments.length) {
        answer.comments.splice(index, 1);
      }
    } catch (error) {
      this.handleError(error, "deleteComment");
    }
  }
}
