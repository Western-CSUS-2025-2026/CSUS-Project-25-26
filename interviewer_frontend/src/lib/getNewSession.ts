import { Grading, Session, StagingSession } from "@/types/session";
import { fetchAPIAuthorized } from "./fetchAuth";
import { defaultTemplate } from "@/types/template";

export async function getSessionNew(
  id: number,
): Promise<{ success: false } | { success: true; session: Session }> {
  const res = await fetchAPIAuthorized(
    `sessions/${id}?include=grades&include=questions&include=feedback&include=video`,
    { method: "GET" },
  );

  if (!res.success) {
    console.log("unable to get session");
    return { success: false };
  }
  const staging: StagingSession = res.body;

  const grades: Grading[] = staging.session_components.map((t) => {
    return {
      question: t.question.question,
      overallGrade:
        (t.grade.body_language_score +
          t.grade.brevity_score +
          t.grade.speech_score +
          t.grade.material_score) /
        4,
      scores: [
        {
          title: "Body Language",
          description: "Hand gestures, eye contant, facial expressions",
          score: t.grade.body_language_score,
        },
        {
          title: "Brevity",
          description:
            "How well your usage of words and the meaning behind them",
          score: t.grade.brevity_score,
        },
        {
          title: "Speech",
          description: "Rate of speech, tone, articulation",
          score: t.grade.speech_score,
        },
        {
          title: "Material",
          description: "The content, do your points and sentances make sense",
          score: t.grade.material_score,
        },
      ],
      feedback: staging.session_components.map((t) => {
        return {
          point: t.feedback.point,
          feedback: t.feedback.ways_to_improve,
        };
      }),
    };
  });
  const overallGrade: Grading = {
    overallGrade: grades
      .map((g) => {
        return g.overallGrade;
      })
      .reduce((prev, curr) => {
        return prev + curr;
      }),
    scores: [
      {
        title: "Body Language",
        description: "Hand gestures, eye contant, facial expressions",
        score: grades
          .map((g) => {
            return g.scores[0].score;
          })
          .reduce((prev, curr) => {
            return prev + curr;
          }),
      },
      {
        title: "Brevity",
        description: "How well your usage of words and the meaning behind them",
        score: grades
          .map((g) => {
            return g.scores[1].score;
          })
          .reduce((prev, curr) => {
            return prev + curr;
          }),
      },
      {
        title: "Speech",
        description: "Rate of speech, tone, articulation",
        score: grades
          .map((g) => {
            return g.scores[2].score;
          })
          .reduce((prev, curr) => {
            return prev + curr;
          }),
      },
      {
        title: "Material",
        description: "The content, do your points and sentances make sense",
        score: grades
          .map((g) => {
            return g.scores[3].score;
          })
          .reduce((prev, curr) => {
            return prev + curr;
          }),
      },
    ],
    feedback: [],
  };

  const session: Session = {
    title: staging.id.toString(),
    template: defaultTemplate,
    overallGrade: overallGrade,
    transcript: staging.session_components
      .map((t) => {
        return t.transcript;
      })
      .join(". "),
    creationDate: staging.create_ts,
    id: staging.id.toString(),
    videos: staging.session_components.map((t) => {
      return { url: t.video.s3_key, id: t.video.id.toString() };
    }),
    grades: grades,
  };

  return { success: true, session: session };
}
