"use client";

import { useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Template } from "@/types/template";
import styles from "./newSessionModal.module.css";
import { Search, X, ChevronLeft, Folder, ChevronRight } from "lucide-react";

type Step = "select" | "confirm";

export default function NewSessionModalClient({
  templates,
  step,
  templateId,
}: {
  templates: Template[];
  step: Step;
  templateId: string;
}) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [query, setQuery] = useState("");

  const selectedTemplate = useMemo(() => {
    return templates.find((t) => t.id === templateId) ?? null;
  }, [templates, templateId]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return templates;
    return templates.filter(
      (t) =>
        t.title.toLowerCase().includes(q) ||
        t.description.toLowerCase().includes(q),
    );
  }, [templates, query]);

  function setParams(next: Record<string, string | null>) {
    const params = new URLSearchParams(searchParams.toString());
    for (const [k, v] of Object.entries(next)) {
      if (v === null) params.delete(k);
      else params.set(k, v);
    }
    router.push(`/sessions?${params.toString()}`);
  }

  function close() {
    setParams({ newSession: null, step: null, templateId: null });
  }

  function goSelect() {
    setParams({ step: "select", templateId: null });
  }

  function chooseTemplate(id: string) {
    setParams({ step: "confirm", templateId: id });
  }

  function startSession() {
    alert("Start New Session (wired later)");
  }

  return (
    <div className={styles.overlay} onMouseDown={close}>
      <div className={styles.modal} onMouseDown={(e) => e.stopPropagation()}>
        <div className={styles.topRow}>
          {step === "confirm" ? (
            <button className={styles.backBtn} onClick={goSelect}>
              <ChevronLeft size={18} strokeWidth={1.5} />
              <span>Back</span>
            </button>
          ) : (
            <div />
          )}

          <button className={styles.closeBtn} onClick={close} aria-label="Close">
            <X size={18} strokeWidth={1.5} />
          </button>
        </div>

        {/* Keeps modal size fixed  */}
        <div className={styles.content}>
          {step === "select" ? (
            <>
              <div className={styles.searchRow}>
                <Search size={18} strokeWidth={1.5} />
                <input
                  className={styles.searchInput}
                  placeholder="Search templates..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
                {query.length > 0 && (
                  <button
                    className={styles.clearBtn}
                    onClick={() => setQuery("")}
                    aria-label="Clear"
                  >
                    <X size={16} strokeWidth={1.5} />
                  </button>
                )}
              </div>

              <div className={styles.list}>
                {filtered.map((t) => (
                  <button
                    key={t.id}
                    className={styles.listItem}
                    onClick={() => chooseTemplate(t.id)}
                  >
                    <div className={styles.itemIcon}>
                      <Folder size={18} strokeWidth={1.5} />
                    </div>

                    <div className={styles.itemText}>
                      <div className={styles.itemTitle}>{t.title}</div>
                      <div className={styles.itemSubtitle}>{t.description}</div>
                    </div>

                    <div className={styles.chevron}>
                      <ChevronRight size={20} strokeWidth={1.5} />
                    </div>
                  </button>
                ))}
              </div>
            </>
          ) : (
            <>
              <h1 className={styles.h1}>Create Session</h1>
              <p className={styles.helpText}>
                Creating a session from a template selects a variety of questions
                from the template, so you can reuse templates and have different
                questions each time.
              </p>

              <h2 className={styles.h2}>Selected Template</h2>

              <div className={styles.selectedCard}>
                <div className={styles.selectedTitle}>
                  {selectedTemplate?.title ?? "Template"}
                </div>
                <div className={styles.selectedSubtitle}>
                  {selectedTemplate?.description ?? ""}
                </div>
              </div>

              <button className={styles.startBtn} onClick={startSession}>
                <span>Start New Session</span>
                <span className={styles.startPlus}>+</span>
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
