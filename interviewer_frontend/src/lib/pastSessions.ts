import { defaultTemplate } from "@/types/template";
import { SimpleSession } from "@/types/simpleSession";
import { fetchAPIAuthorized } from "./fetchAuth";
import { StagingSession } from "@/types/session";

/** Fetches a users past sessions
 */
export async function getPastSessions(): Promise<SimpleSession[]> {
  const res = await fetchAPIAuthorized(
    "sessions?include=questions&include=grades&limit=20&offest=0&include=template",
    {
      method: "GET",
    },
  );

  if (!res.success) {
    console.log(res);
    return [];
  }

  const body: { sessions: StagingSession[] } = res.body;

  const sessions: SimpleSession[] = body.sessions.map((s) => {
    const map = s.session_components.map((comp) => {
      return comp.state;
    });
    if (
      map.includes("PENDING") &&
      Date.now() - new Date(s.create_ts).getTime() > 120 * 1000
    ) {
      return {
        template: {
          title: s.template.job_title,
          description: s.template.description,
          id: s.template.id.toString(),
        },
        createTime: s.create_ts,
        state: "INCOMPLETE",
        title: "Session #" + s.id,
        id: s.id.toString(),
      };
    }
    if (map.every((v) => v == "COMPLETED") == true) {
      const overallGrade =
        s.session_components
          .map((c) => {
            return (
              (c.grade.speech_score +
                c.grade.brevity_score +
                c.grade.body_language_score +
                c.grade.material_score) /
              4 /
              10
            );
          })
          .reduce((prev, curr) => {
            return prev + curr;
          }) / s.session_components.length;
      return {
        overallGrade: overallGrade,
        state: "COMPLETED",
        createTime: s.create_ts,
        id: s.id.toString(),
        title: "Session #" + s.id,
        template: {
          title: s.template.job_title,
          description: s.template.description,
          id: s.template.id.toString(),
        },
      };
    }

    return {
      title: "Session #" + s.id,
      state: "PROCESSING",
      id: s.id.toString(),
      createTime: s.create_ts,
      template: {
        title: s.template.job_title,
        description: s.template.description,
        id: s.template.id.toString(),
      },
    };
  });

  return sessions;
}
