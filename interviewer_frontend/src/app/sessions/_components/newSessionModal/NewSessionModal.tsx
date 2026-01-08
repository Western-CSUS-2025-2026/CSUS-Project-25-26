import { getTemplates } from "@/lib/getTemplates";
import { Template } from "@/types/template";
import NewSessionModalClient from "./NewSessionModalClient";

export default async function NewSessionModal({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  const isOpen = searchParams.newSession === "1";
  if (!isOpen) return null;

  const step = (searchParams.step as string) ?? "select";
  const templateId = (searchParams.templateId as string) ?? "";

  const templates: Template[] = await getTemplates();

  return (
    <NewSessionModalClient
      templates={templates}
      step={step === "confirm" ? "confirm" : "select"}
      templateId={templateId}
    />
  );
}
