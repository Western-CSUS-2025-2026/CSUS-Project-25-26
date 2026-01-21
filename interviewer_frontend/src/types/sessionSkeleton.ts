import { defaultTemplate, Template } from "./template";

// this will be used on the recording screen to display
// info about the current session
export interface SessionSkeleton {
  id: string;
  title: string;
  template: Template;
  questions: string[];
  // this is the number of videos uploaded under this session id
  numberOfUploadedVideos: number;
}

export const defaultSessionSkeleton: SessionSkeleton = {
  title: "Session #13",
  id: " this is an id",
  template: defaultTemplate,
  questions: [
    "Whats your greatest strength?",
    "Whens a time where you had to think on your feet?",
    "What makes you perfect for this role?",
  ],
  numberOfUploadedVideos: 1,
};
