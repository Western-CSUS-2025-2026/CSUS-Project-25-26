import { Suspense } from "react";
import styles from "./page.module.css";
import { getSessionNew } from "@/lib/getNewSession";
import SessionOverviewContent from "@/app/session-overview/SessionOverviewContent";

async function SessionOverview({ params }: { params: { id: string } }) {
  const { id } = params;

  return (
    <div className={styles.container}>
      <Suspense fallback={"loading"}>
        <SessionString id={id}></SessionString>
      </Suspense>
    </div>
  );
}

async function SessionString(props: { id: string }) {
  console.log(props.id);

  const sessions = await getSessionNew(Number(props.id));

  if (sessions.success) {
    return <SessionOverviewContent session={sessions.session} />;
  } else {
    return <div>{"Error"}</div>;
  }
}

export default SessionOverview;