import { BaseService } from "./base.service";
// import type { IQuestion } from "@/interfaces/models";

export default class QuestionsService extends BaseService {
  public isProcessing = false;

  /**
   * Retrieves all questions.
   * @returns Array of questions.
   */
  // async getQuestions(): Promise<IQuestion[]> {
  //   try {
  //     // TODO: Replace with actual API call
  //     return this.questions;
  //   } catch (error) {
  //     this.handleError(error, "QuestionsService.getQuestions()");
  //     return [];
  //   }
  // }

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

      alert(`File "${file.name}" uploaded successfully!`);
    } catch (error) {
      this.handleError(error, "handleFileUpload");
    } finally {
      this.isProcessing = false;
    }
  }
}
