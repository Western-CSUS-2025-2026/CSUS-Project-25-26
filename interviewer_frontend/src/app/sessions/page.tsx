import Link from "next/link";
import styles from "./page.module.css";
import PastSessionsGrid from "./_components/pastSessions/pastSessions";
import RecentTemplates from "./_components/recentTemplates/recentTemplates";

import Modal from "@/components/modal/modal";

type SearchParamProps = {
  searchParams: Record<string, string> | null | undefined;
};

async function SessionPage({ searchParams }: SearchParamProps) {
  const resolvedParams = await searchParams;

  const show = resolvedParams?.show;
  return (
    <div className={styles.sessionPageContainer}>
      <Link href={"/sessions?show=true"}>Show modal</Link>

      {/* Remove this and replace with recent templates component */}
      <section className={styles.recentTemplatesContainer}>
        <RecentTemplates />
      </section>


      {/* remove this component and replace with past sessions component */}
      <section className={styles.pastSessionsContainer}>
        <PastSessionsGrid />
      </section>

      {/* This is where the modal is going to appear */}
      {show && <Modal height="20em" width="20em" />}
    </div>
  );
}

export default SessionPage;
