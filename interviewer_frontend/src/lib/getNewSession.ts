import { RawSession } from "@/types/simpleSession";
import { fetchAPIAuthorized } from "./fetchAuth";

export async function getSessionNew(
  id: number,
): Promise<{ success: false } | { success: true; session: RawSession }> {
  const res = await fetchAPIAuthorized(
    `sessions/${id}?include=grades&include=questions&include=feedback&include=video`,
    { method: "GET" },
  );

  if (!res.success) {
    console.log("unable to get session");
    return { success: false };
  }

  const body = res.body;
  return { success: true, session: body };
}
