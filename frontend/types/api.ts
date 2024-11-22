/* eslint-disable @typescript-eslint/no-explicit-any */
import type { UUID } from "crypto";

export interface APIResponse<T> {
  data?: T;
  error?: {
    message: string;
    details?: any;
  };
}

export interface ApiError {
  status: number;
  message: string;
  details?: unknown;
}

export interface TimeStampSchema {
  created_at: Date;
}

export interface IdSchema {
  id: UUID;
}

// Chain Types
export interface Chain extends TimeStampSchema, IdSchema {
  file_name: string;
}

export interface AvailableChain {
  file_name: string;
}

export interface ChainSelection {
  file_names: string[];
}

// Configuration Types
export interface ConfigurationBase {
  prompt_template?: Record<string, any>;
  llm_parameters?: Record<string, any>;
}

export interface Configuration extends ConfigurationBase, TimeStampSchema, IdSchema {}

export type ConfigurationCreate = ConfigurationBase;
export type ConfigurationUpdate = Partial<ConfigurationBase>;

// Answer Comment Types
export interface AnswerCommentBase {
  answer_id: UUID;
  comment_text: string;
}

export interface AnswerComment extends AnswerCommentBase, TimeStampSchema, IdSchema {
  last_modified: Date;
}

export type AnswerCommentCreate = AnswerCommentBase;
export interface AnswerCommentUpdate {
  comment_text: string;
}

// Answer Types
export interface AnswerBase {
  question_id: UUID;
  chain_id: UUID;
  configuration_id: UUID;
  generated_answer: string;
  score?: number;
}

export interface Answer extends AnswerBase, TimeStampSchema, IdSchema {}

export interface AnswerDetail extends Answer {
  comments: AnswerComment[];
}

export type AnswerCreate = AnswerBase;
export interface AnswerBulkCreate {
  answers: AnswerCreate[];
}

export interface AnswerUpdate {
  score?: number;
}

// Question Types
export interface QuestionBase {
  question_text: string;
  expected_answer?: string;
}

export interface Question extends QuestionBase, TimeStampSchema, IdSchema {
  last_modified: Date;
}

export interface QuestionDetail extends Question {
  answers: AnswerDetail[];
}

export type QuestionCreate = QuestionBase;

export type QuestionUpdate = Partial<QuestionBase>;

export interface QuestionBulkDelete {
  question_ids: UUID[];
}

// Session Types
export interface SessionBase {
  name: string;
  description?: string;
}

export interface Session extends SessionBase, TimeStampSchema, IdSchema {
  last_modified: Date;
}

export interface SessionDetail extends Session {
  chains: Chain[];
  questions: QuestionDetail[];
  configurations: Configuration[];
}

export type SessionCreate = SessionBase;
export type SessionUpdate = Partial<SessionBase>;
