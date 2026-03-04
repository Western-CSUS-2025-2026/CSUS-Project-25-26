import { Template } from "@/types/template";
import { fetchAPIAuthorized } from "./fetchAuth";

/**
 * Gets a list of all the available templates
 **/
export async function getTemplates(): Promise<Template[]> {
  const res = await fetchAPIAuthorized("templates", {
    method: "GET",
  });

  if (!res.success) {
    console.log("Unable to get");
    console.log(res);
    return [];
  }

  const templates: { job_title: string; description: string; id: number }[] =
    res.body;

  const mapped: Template[] = templates.map((t) => {
    return {
      title: t.job_title,
      description: t.description,
      id: t.id.toString(),
    };
  });

  return mapped;
}
