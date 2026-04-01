import { sleep } from "./sleep";
import { defaultSession, Session } from "@/types/session";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export async function getSessionById(id: string): Promise<Session> {
  // replace with network call
  await sleep(2000);
  return defaultSession;
}
