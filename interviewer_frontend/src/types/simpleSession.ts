import { defaultGrading, Grading } from "./session";
import { defaultTemplate, Template } from "./template";

export type SimpleSession = ProcessingSession | CompletedSession;
// a processing Session that does not contain any data
export interface ProcessingSession {
  state: "PROCESSING";
  template: Template;
  createTime: string;
}
export interface CompletedSession {
  state: "COMPLETED";
  template: Template;
  createTime: string;
  overallGrade: Grading;
}

export const defaultCompletedSimpleSession: SimpleSession = {
  state: "COMPLETED",
  template: defaultTemplate,
  createTime: Date().toString(),
  overallGrade: defaultGrading,
};
export const defaultProcessingSimpleSession: ProcessingSession = {
  state: "PROCESSING",
  template: defaultTemplate,
  createTime: Date().toString(),
};
