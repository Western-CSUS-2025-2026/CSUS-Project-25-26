import { fetchAPIAuthorized } from "../fetchAuth";

export interface Question {
  question: string;
  id: number;
  template_id: number;
  component_id: number;
}
export async function getQuestions(
  templeteId: number,
): Promise<{ questions: Question[]; success: true } | { success: false }> {
  const res = await fetchAPIAuthorized(`questions/template/${templeteId}`, {
    method: "GET",
  });

  if (!res.success) {
    console.log("Getting questions failed");
    console.log(res);
    return { success: false };
  }
  const body: Question[] = res.body;

  return { success: true, questions: body };
}
