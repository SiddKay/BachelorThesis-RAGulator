import type { UUID } from "crypto";

export interface Session {
  id: UUID;
  name: string;
  description?: string;
  created_at: string;
  last_modified: string;
  chains: Chain[];
  questions: Question[];
  configurations: Configuration[];
}

export interface Chain {
  id: UUID;
  file_name: string;
  session_id: UUID;
  created_at: string;
}

export interface Configuration {
  id: UUID;
  session_id: UUID;
  prompt_template?: Record<string, string | number | boolean>;
  llm_parameters?: Record<string, string | number | boolean>;
  created_at: string;
}

export interface Question {
  id: UUID;
  session_id: UUID;
  question_text: string;
  expected_answer?: string;
  created_at: string;
  last_modified: string;
  answers?: Answer[];
}

export interface Answer {
  id: UUID;
  chain_id: UUID;
  question_id: UUID;
  configuration_id: UUID;
  generated_answer: string;
  score?: number;
  created_at: string;
  comments?: AnswerComment[];
}

export interface AnswerComment {
  id: UUID;
  answer_id: UUID;
  comment_text: string;
  created_at: string;
  last_modified: string;
}
