import Card from "@/components/card/card";
import styles from "./summary.module.css";
import InvertedPlusIcon from "@/components/icons/invertedPlusIcon";
import { convertToLetterGrade } from "@/components/gauge/gauge";
import { Session } from "@/types/session";

export default function Summary({ session }: { session: Session }) {
  return (
    <div className={styles.row}>

      {/* QUESTIONS CARD */}
      <Card>
        <div className={styles.questionsCard}>
          <div className={styles.row2}>
            <h1 className={styles.questionTitle}>Questions</h1>

            <button type="button" aria-label="Add" className={styles.plusButton}>
              <InvertedPlusIcon
                foreground="#202020"
                background="#cb9fe6"
                size="40px"
              />
            </button>
          </div>

          <p className={styles.questionSub}>
            The questions you answered in order.
          </p>

          <div>
            {session.grades.map((g, index) => (
              <div key={index}>
                <p>{g.question}</p>
              </div>
            ))}
          </div>
        </div>
      </Card>

      {/* GRADE CARD */}
      <div className="gradeCardOverride">
        <style>{`
          .gradeCardOverride .cardStyle {
            background-color: #cb9fe6 !important;
          }
        `}</style>

        <Card>
          <div className={styles.gradeCard}>
            <h1>Grade</h1>
            <p className={styles.gradeSub}>
              An associated letter grade
            </p>

            <h1 className={styles.letterGrade}>
              {convertToLetterGrade(session.overallGrade.overallGrade)}
            </h1>
          </div>
        </Card>
      </div>

    </div>
  );
}