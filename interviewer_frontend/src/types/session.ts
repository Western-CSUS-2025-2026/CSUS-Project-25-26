import { defaultTemplate, Template } from "./template";

// A completed session that has been processed and contains all the data
export interface Session {
  title: string;
  template: Template;
  overallGrade: Grading;
  grades: Grading[];
  transcript: string;
  creationDate: string;
  videos: SessionVideo[];
  id: string;
}

// a video of the session
interface SessionVideo {
  url: string;
  question: string;
}

// the grading scheme
export interface Grading {
  // this will be undefined when it is an overall grade
  question?: string;
  overallGrade: number;
  // scores for the individual categories
  scores: Score[];
  feedback: Feedback[];
}
// a single score for an individual category
interface Score {
  title: string;
  description: string;
  score: number;
}
// the feedback
interface Feedback {
  // the skill or thing that they need work on
  point: string;
  // a list of ways to improve apon the point
  feedback: string[];
}
export const defaultGrading: Grading = {
  question: "What is your greatest strength?",
  overallGrade: 0.6,
  scores: [
    {
      title: "Body Language",
      description: "Hand gestures, eye contant, facial expressions",
      score: 0.3,
    },
    {
      title: "Brevity",
      description: "How well your usage of words and the meaning behind them",
      score: 0.8,
    },
    {
      title: "Speech",
      description: "Rate of speech, tone, articulation",
      score: 1,
    },
    {
      title: "Material",
      description: "The content, do your points and sentances make sense",
      score: 0.2,
    },
  ],
  feedback: [
    {
      point: "Speaking too fast",
      feedback: [
        "Try articulating your words more to slow yourself down",
        "Try taking longer breaks between sentances and words",
      ],
    },
    {
      point: "Over usage of filler words",
      feedback: [
        "Take pauses instead of using the filler words",
        "Think about the entire sentance before saying it to reduce the need for filler words",
      ],
    },
  ],
};

export const defaultSession: Session = {
  title: "Session #1",
  id: "this is an id",
  creationDate: Date().toString(),
  overallGrade: defaultGrading,
  template: defaultTemplate,
  grades: [defaultGrading, defaultGrading, defaultGrading],
  videos: [
    {
      url: "this is a test url",
      question: "What is your greatest weakness?",
    },
  ],
  transcript:
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse eu odio vitae tortor maximus blandit. Morbi posuere fermentum nulla, ut sagittis eros commodo pellentesque.Aenean lacinia consequat imperdiet. Pellentesque sit amet neque eget lorem euismod sagittis. Nam sed egestas eros. Proin vel tellus orci. Mauris sit amet molestie dolor. Aenean mi nisl, interdum sed mi vitae, feugiat laoreet odio.Aliquam pharetra metus sed augue cursus, vel feugiat tellus cursus. Pellentesque hendrerit a nunc nec pellentesque. Proin a odio tempus, blandit elit vitae, vehicula nunc. Morbi in ex eu sapien viverra viverra id id massa. Pellentesque eget mollis lectus. In ac risus neque. Pellentesque libero sem, cursus non condimentum imperdiet,dictum in diam. Quisque felis sapien, volutpat non quam quis, euismod efficitur neque. Morbi bibendum elementum erat. Vestibulum quis porttitor justo. Nam suscipit nibh sit amet pulvinar interdum. Morbi suscipit, libero in dapibus tincidunt, lacus quam posuere mi, eget pulvinar dui ligula at dui. Ut luctus odio id ante euismod volutpat. Sed ut suscipit velit.",
};
