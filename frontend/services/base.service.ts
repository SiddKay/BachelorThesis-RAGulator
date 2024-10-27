export abstract class BaseService {
  protected handleError(error: Error | unknown, context: string) {
    console.error(`Error in ${context}:`, error);
    throw error;
  }

  protected async delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
