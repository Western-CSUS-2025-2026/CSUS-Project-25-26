import { defaultTemplate } from "@/types/template";
import { RawSession, SimpleSession } from "@/types/simpleSession";
import { defaultGrading } from "@/types/session";
import { fetchAPIAuthorized } from "./fetchAuth";

/** Fetches a users past sessions
 */
export async function getPastSessions(): Promise<SimpleSession[]> {
  // eventaully will be populated with a network call
  const res = await fetchAPIAuthorized(
    "sessions?include=questions&limit=20&offest=0",
    {
      method: "GET",
    },
  );

  if (!res.success) {
    console.log(res);
    return [];
  }

  const body: { sessions: RawSession[] } = res.body;

  const sessions: SimpleSession[] = body.sessions.map((s) => {
    if (s.session_components != undefined) {
      const map = s.session_components.map((comp) => {
        return comp.state == "PENDING";
      });
      if (map.includes(true)) {
        return {
          title: "Session #" + s.id,
          state: "PROCESSING",
          id: s.id.toString(),
          createTime: s.create_ts,
          template: defaultTemplate,
        };
      }
    }
    return {
      overallGrade: s.overall_grade,
      state: "COMPLETED",
      createTime: s.create_ts,
      id: s.id.toString(),
      title: "Session #" + s.id,
      template: defaultTemplate,
    };
  });

  return sessions;
}
