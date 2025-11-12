import { sleep } from "./sleep";
import {
  defaultCompletedSimpleSession,
  defaultProcessingSimpleSession,
  SimpleSession,
} from "@/types/simpleSession";

/** Fetches a users past sessions
 */
export async function getPastSessions(): Promise<SimpleSession[]> {
  // eventaully will be populated with a network call
  await sleep(2000);

  return [
    defaultProcessingSimpleSession,
    defaultCompletedSimpleSession,
    defaultCompletedSimpleSession,
    defaultCompletedSimpleSession,
    defaultCompletedSimpleSession,
    defaultCompletedSimpleSession,
  ];
}
