import { defaultTemplate, Template } from "@/types/template";
import { sleep } from "./sleep";

/**
 * Gets a list of all the available templates
 **/
export async function getTemplates(): Promise<Template[]> {
  // will replace with network call
  await sleep(2000);
  return [
    defaultTemplate,
    defaultTemplate,
    defaultTemplate,
    defaultTemplate,
    defaultTemplate,
    defaultTemplate,
    defaultTemplate,
  ];
}
