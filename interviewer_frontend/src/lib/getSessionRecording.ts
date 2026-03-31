import { StagingSession } from "@/types/session";
import { fetchAPIAuthorized } from "./fetchAuth";

export async function getSessionRecording(
  id: number,
): Promise<{ success: false } | { success: true; session: StagingSession }> {
  const res = await fetchAPIAuthorized(
    `sessions/${id}?include=grades&include=questions`,
    { method: "GET" },
  );

  if (!res.success) {
    console.log("unable to get session");
    return { success: false };
  }
  const staging: StagingSession = res.body;
  return { success: true, session: staging };
}
