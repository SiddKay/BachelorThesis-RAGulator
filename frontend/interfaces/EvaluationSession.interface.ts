/**
 * Represents a question in an evaluation session.
 * Questions are part of a question set.
 *
 * @interface IQuestion
 *
 * @property {number} id - Unique identifier for the question.
 * @property {string} text - Text of the question.
 * @property {boolean} important - Indicates whether the question is important.
 * @property {IAnswer[]} answers - Array of answers to the question.
 * @property {string} expectedAnswer - Expected answer to the question.
 * @property {number} questionSetId - Identifier for the set of questions that the question belongs to.
 */
interface IQuestion {
  id: number;
  text: string;
  important: boolean;
  answers: IAnswer[];
  expectedAnswer?: string;
  questionSetId?: number;
}

/**
 * Represents an answer to a question in an evaluation session.
 *
 * @interface IAnswer
 *
 * @property {number} id - Unique identifier for the answer.
 * @property {number} questionId - Identifier for the question that the answer is related to.
 * @property {number} configVersion - Identifier for the configuration that the answer is related to.
 * @property {string} text - Text of the answer.
 * @property {string[]} comments - Array of comments that the user has added to the answer.
 * @property {number} score - Score that the user has given to the answer.
 */
interface IAnswer {
  id: number;
  questionId: number;
  configVersion: number; // config id
  text: string;
  comments?: string[];
  score?: number;
}

/**
 * Represents a configuration that the user has tried during an evaluation session.
 *
 * @interface IConfig
 *
 * @property {number} id - Unique identifier for the configuration.
 * @property {Record<string, string | number | boolean>} params - Dynamically holds parameters for runnables.
 * @property {Date} createdAt - Date and time when the configuration was created.
 */
interface IConfig {
  id: number;
  params: Record<string, string | number | boolean>;
  createdAt: Date;
}

/**
 * Represents an evaluation session.
 *
 * @interface IEvaluationSession
 *
 * @property {string} sessionId - Unique identifier for the session.
 * @property {number} questionSetId - Identifier for the set of questions used in the session.
 * @property {IQuestion[]} questions - Array of questions included in the session.
 * @property {IConfig[]} configs - Array of configurations that the user has tried during the session.
 */
interface IEvaluationSession {
  sessionId: string;
  questionSetId: number;
  questions: IQuestion[];
  configs: IConfig[]; // all the configs user has tried
}

export type { IQuestion, IAnswer, IConfig, IEvaluationSession };
