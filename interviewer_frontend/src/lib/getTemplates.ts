import { defaultTemplate, Template } from "@/types/template";
import { sleep } from "./sleep";
import { fetchAPI } from "./fetch";

/**
 * Gets a list of all the available templates
 **/
export async function getTemplates(): Promise<Template[]> {
  // will replace with network call
  await sleep(2000);

  const res = await fetchAPI("templates", {});

  if (!res.ok) {
    console.log("Unable to get");
    console.log(res);
    return [];
  }

  const templates: { job_title: string; description: string; id: number }[] =
    await res.json();

  const mapped: Template[] = templates.map((t) => {
    return {
      title: t.job_title,
      description: t.description,
      id: t.id.toString(),
    };
  });

  return mapped;
}
