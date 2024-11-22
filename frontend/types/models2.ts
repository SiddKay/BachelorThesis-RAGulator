/**
 * Represents a single evaluation Session.
 * @property {string} name - The name of the session.
 * @property {string} description - The description of the session.
 */
export interface ISession {
  name: string;
  description?: string;
}

/**
 * Represents a single Chain.
 * @property {string} file_name - The name of the chain file.
 */
export interface IChain {
  file_name: string;
}

/**
 * Represents a Configuration passed to the chain when invoked.
 * @property {Record<string, string | number | boolean>} prompt_template - The prompt template for the chain.
 * @property {Record<string, string | number | boolean>} llm_parameters - The LLM parameters for the chain model.
 */
export interface IConfiguration {
  prompt_template?: Record<string, string | number | boolean>;
  llm_parameters?: Record<string, string | number | boolean>;
}

/**
 * Represents a single Question.
 * @property {string} question_text - The question text.
 * @property {string} expected_answer - The expected answer for the question, for reference.
 * @property {IAnswer[]} answers - The answers generated for the question.
 */
export interface IQuestion {
  question_text: string;
  expected_answer?: string;

  // TODO: Remove this since it's not needed in the frontend once the API has been connected.
  answers?: IAnswer[];
}

// TODO: Remove this whole Interface it's not needed in the frontend once the API has been connected.
/**
 * Represents a single Answer.
 * @property {string} id - AnswerID
 * @property {string} chain_id - The ChainID of the chain for which the answer is generated.
 * @property {string} question_id - The QuestionID of the question for which the answer is generated.
 * @property {string} configuration_id - The ConfigurationID of the configuration used to generate the answer.
 * @property {string} generated_answer - The generated answer.
 * @property {number} score - The score of the answer.
 * @property {string} created_at - The date and time the answer was created.
 * @property {IAnswerComment[]} comments - The comments associated with the answer.
 */
export interface IAnswer {
  id: string;
  chain_id: string;
  question_id: string;
  configuration_id: string;
  generated_answer: string;
  score?: number;
  created_at: string;
  comments?: IAnswerComment[];
}

/**
 * Represents a single Answer Comment.
 * @property {string} answer_id - The AnswerID the comment is associated with.
 * @property {string} comment_text - The comment text.
 */
export interface IAnswerComment {
  answer_id: string;
  comment_text: string;
}
