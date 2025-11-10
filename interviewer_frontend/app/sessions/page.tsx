// app/sessions/page.tsx
import { Suspense } from "react";
import RecentTemplates from "./_components/recentTemplates/RecentTemplates";

export default function SessionsPage() {
  return (
    <main style={{ padding: "2rem" }}>
      <h1 style={{ fontSize: "1.5rem", marginBottom: "1rem" }}>Sessions</h1>
      <Suspense fallback={<p>Loading recent templates...</p>}>
        <RecentTemplates />
      </Suspense>
    </main>
  );
}
