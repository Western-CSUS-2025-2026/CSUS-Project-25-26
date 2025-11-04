import Card from "@/components/card/card";
import GradeOverview from "./_components/gradeOverview/gradeOverview";
import QuestionOverview from "./_components/questionOverview/questionOverview";
import styles from "./page.module.css";

function SessionOverview() {
  return (
    <div className={styles.container}>
      <div className={styles.leftColumn}>
        <div className={styles.topContainer}>
          <QuestionOverview></QuestionOverview>
          <GradeOverview></GradeOverview>
        </div>
      </div>
      <div className={styles.rightColumn}>
        <h1>Recording</h1>
        <Card height="10em"></Card>
        <h1>Transcript</h1>
        <Card height="15em"></Card>
      </div>
    </div>
  );
}

export default SessionOverview;
