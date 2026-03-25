import { defaultGrading, Grading } from "./session";
import { defaultTemplate, Template } from "./template";

export type RawSession = {
  id: number;
  user_id: number;
  overall_grade: number;
  create_ts: string;
  session_components: {
    id: number;
    transcript: string;
    state: string;
    question_id: number;
    question: {
      question: string;
      id: number;
      template_id: number;
    };
    grade: {
      id: number;
      body_language_score: number;
      speech_score: number;
      material_score: number;
      brevity_score: number;
    };
    feedback: {
      id: number;
      point: string;
      ways_to_improve: string;
    };
    video: {
      id: number;
      s3_key: string;
    };
  }[];
};

export type SimpleSession = ProcessingSession | CompletedSession;
// a processing Session that does not contain any data
export interface ProcessingSession {
  title: string;
  state: "PROCESSING";
  template: Template;
  createTime: string;
  id: string;
}
export interface CompletedSession {
  title: string;
  state: "COMPLETED";
  template: Template;
  createTime: string;
  overallGrade: number;
  id: string;
}

export const defaultCompletedSimpleSession: SimpleSession = {
  title: "Session #1",
  state: "COMPLETED",
  template: defaultTemplate,
  createTime: Date().toString(),
  overallGrade: 0.8,
  id: "this is an id",
};
export const defaultProcessingSimpleSession: ProcessingSession = {
  title: "Session #1",
  state: "PROCESSING",
  template: defaultTemplate,
  createTime: Date().toString(),
  id: "this is an id",
};
