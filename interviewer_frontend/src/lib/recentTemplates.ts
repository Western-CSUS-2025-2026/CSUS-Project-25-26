import { defaultTemplate, Template } from "@/types/template";
import { sleep } from "./sleep";

export async function getRecentTemplates(): Promise<Template[]> {
  // will have a network request eventually

  await sleep(1000);
  return [defaultTemplate, defaultTemplate];
}
