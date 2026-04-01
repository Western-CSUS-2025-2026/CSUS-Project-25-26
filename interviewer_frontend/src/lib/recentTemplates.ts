import { Template } from "@/types/template";
import { getTemplates } from "./getTemplates";

export async function getRecentTemplates(): Promise<Template[]> {
  // will have a network request eventually
  const temps = await getTemplates();

  return temps.slice(0, 2);
}
