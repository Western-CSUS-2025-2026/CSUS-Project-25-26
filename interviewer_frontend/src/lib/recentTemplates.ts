import { defaultTemplate, Template } from "@/types/template";
import { sleep } from "./sleep";
import { getTemplates } from "./getTemplates";

export async function getRecentTemplates(): Promise<Template[]> {
  // will have a network request eventually
  const temps = await getTemplates();

  return [temps[0], temps[1]];
}
