import { sleep } from "./sleep";
import { defaultSession, Session } from "@/types/session";

export async function getSessionById(id: string): Promise<Session> {
  // replace with network call
  await sleep(2000);
  return defaultSession;
}
