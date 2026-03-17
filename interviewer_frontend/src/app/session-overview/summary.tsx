import Card from "@/components/card/card";
import styles from "./summary.module.css";
import { getSessionInfo } from "@/lib/getSessionInfo"; 
import InvertedPlusIcon from "@/components/icons/invertedPlusIcon";
import { defaultGrading, defaultSession } from "@/types/session";
import {convertToLetterGrade} from "@/components/gauge/gauge";


export default async function Summary() {
    const session = await getSessionInfo();

    return (
        <div className={styles.row}> 

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
                        {session.questions.map((q, index) => (
                            <p key={index}>{q}</p>
                        ))}
                    </div>
                </div>
            </Card>

            {/* Grade Card with override */}
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
                            {convertToLetterGrade(defaultGrading.overallGrade)}
                        </h1>
                    </div>
                </Card>
            </div>

        </div>
    );
}