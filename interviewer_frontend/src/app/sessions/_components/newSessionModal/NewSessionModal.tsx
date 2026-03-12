"use client";

import { useEffect, useState } from "react";
import { Template } from "@/types/template";
import NewSessionModalClient from "./NewSessionModalClient";
import { useSearchParams } from "next/navigation";

type Step = "select" | "confirm";

function readParams() {
  const params = new URLSearchParams(window.location.search);

  const isOpen = params.get("newSession") === "1";
  const step = (params.get("step") as Step) || "select";
  const templateId = params.get("templateId") || "";

  return { isOpen, step, templateId };
}

export default function NewSessionModal({
  templates,
}: {
  templates: Template[];
}) {
  const [state, setState] = useState(() => ({
    isOpen: false,
    step: "select" as Step,
    templateId: "",
  }));
  const params = useSearchParams();

  useEffect(() => {
    const update = () => setState(readParams());

    update();
  }, [params]);

  if (!state.isOpen) return null;

  return (
    <NewSessionModalClient
      loading={false}
      templates={templates}
      step={state.step}
      templateId={state.templateId}
    />
  );
}
