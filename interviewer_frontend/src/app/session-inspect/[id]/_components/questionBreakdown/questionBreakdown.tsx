import Card from "@/components/card/card";
import Gauge from "@/components/gauge/gauge";
import { Grading } from "@/types/session";
import styles from "./questionBreakdown.module.css";

interface QuestionBreakdownProps {
  grading: Grading;
}

export default function QuestionBreakdown({ grading }: QuestionBreakdownProps) {
  return (
    <div className={styles.questionSection}>
      <h2 className={styles.questionTitle}>{grading.question}</h2>

      <div className={styles.content}>
        <Card>
          <div className={styles.gradeCard}>
            <div className={styles.header}>
              <h3 className={styles.title}>Grade</h3>
              <p className={styles.subtitle}>An associated letter grade</p>
            </div>
            <div className={styles.gaugeContainer}>
              <Gauge score={grading.overallGrade} />
            </div>
          </div>
        </Card>

        <Card>
          <div className={styles.skillsCard}>
            <h3 className={styles.skillsTitle}>Skills Breakdown</h3>

            <div className={styles.barsContainer}>
              {grading.scores.map((score, index) => (
                <div key={index} className={styles.barItem}>
                  <div className={styles.barWrapper}>
                    <div className={styles.bar}>
                      <div
                        className={styles.barFill}
                        style={{ height: `${score.score * 100}%` }}
                      />
                    </div>
                  </div>
                  <span className={styles.barLabel}>{score.title}</span>
                </div>
              ))}
            </div>
          </div>
        </Card>

        <Card>
          <div className={styles.feedbackCard}>
            <div className={styles.feedbackHeader}>
              <h3 className={styles.feedbackTitle}>Feedback</h3>
              <p className={styles.feedbackSubtitle}>
                Your next steps for improving your skills
              </p>
            </div>

            <div className={styles.feedbackGrid}>
              {grading.feedback.map((item, index) => (
                <div key={index} className={styles.feedbackItem}>
                  <h4 className={styles.feedbackPoint}>{item.point}</h4>
                  <ul className={styles.suggestionsList}>
                    {item.feedback.map((suggestion, idx) => (
                      <li key={idx} className={styles.suggestion}>
                        {suggestion}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}