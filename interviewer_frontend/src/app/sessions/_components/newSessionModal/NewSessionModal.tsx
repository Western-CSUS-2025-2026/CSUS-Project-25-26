"use client";

import { useEffect, useMemo, useState } from "react";
import { Template } from "@/types/template";
import NewSessionModalClient from "./NewSessionModalClient";

type Step = "select" | "confirm";

function readParams() {
  const params = new URLSearchParams(window.location.search);

  const isOpen = params.get("newSession") === "1";
  const step = (params.get("step") as Step) || "select";
  const templateId = params.get("templateId") || "";

  return { isOpen, step, templateId };
}

export default function NewSessionModal({ templates }: { templates: Template[] }) {
  const [state, setState] = useState(() => ({
    isOpen: false,
    step: "select" as Step,
    templateId: "",
  }));

  useEffect(() => {
    const update = () => setState(readParams());

    // initial read
    update();

    // back/forward
    window.addEventListener("popstate", update);

    // our custom event (pushState)
    window.addEventListener("urlchange", update);

    return () => {
      window.removeEventListener("popstate", update);
      window.removeEventListener("urlchange", update);
    };
  }, []);

  if (!state.isOpen) return null;

  return (
    <NewSessionModalClient
      templates={templates}
      step={state.step}
      templateId={state.templateId}
    />
  );
}
