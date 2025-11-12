import { defaultGrading, Grading } from "./session";
import { defaultTemplate, Template } from "./template";

export type SimpleSession = ProcessingSession | CompletedSession;
// a processing Session that does not contain any data
export interface ProcessingSession {
  title: string;
  state: "PROCESSING";
  template: Template;
  createTime: string;
}
export interface CompletedSession {
  title: string;
  state: "COMPLETED";
  template: Template;
  createTime: string;
  overallGrade: Grading;
}

export const defaultCompletedSimpleSession: SimpleSession = {
  title: "Session #1",
  state: "COMPLETED",
  template: defaultTemplate,
  createTime: Date().toString(),
  overallGrade: defaultGrading,
};
export const defaultProcessingSimpleSession: ProcessingSession = {
  title: "Session #1",
  state: "PROCESSING",
  template: defaultTemplate,
  createTime: Date().toString(),
};
