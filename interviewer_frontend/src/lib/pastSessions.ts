import { defaultTemplate } from "@/types/template";
import { SimpleSession } from "@/types/simpleSession";
import { fetchAPIAuthorized } from "./fetchAuth";
import { StagingSession } from "@/types/session";

/** Fetches a users past sessions
 */
export async function getPastSessions(): Promise<SimpleSession[]> {
  // eventaully will be populated with a network call
  await sleep(2000);

  if (!res.success) {
    console.log(res);
    return [];
  }

  const body: { sessions: StagingSession[] } = res.body;

  const sessions: SimpleSession[] = body.sessions.map((s) => {
    if (s.session_components != undefined) {
      const map = s.session_components.map((comp) => {
        return comp.state == "PENDING" || comp.state == "INDEXING";
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
