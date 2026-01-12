import styles from "./page.module.css";
import { getSessionById } from "@/lib/getSessionById";
import GradeCard from "./_components/gradeCard/gradeCard";
import QuestionsList from "./_components/questionsList/questionsList";
import SkillsBreakdown from "./_components/skillsBreakdown/skillsBreakdown";
import Feedback from "./_components/feedback/feedback";
import Transcript from "./_components/transcript/transcript";
import Video from "./_components/video/video";
import QuestionBreakdown from "./_components/questionBreakdown/questionBreakdown";
import Breadcrumb from "./_components/breadcrumb/breadcrumb";

async function SessionOverview({ params }: { params: { id: string } }) {
  const session = await getSessionById(params.id);

  // Extract questions from the grades array
  const questions = session.grades
    .map(grade => grade.question)
    .filter((q): q is string => q !== undefined);

  return (
    <div className={styles.pageWrapper}>
      <Breadcrumb sessionId={params.id} />
      
      <div className={styles.container}>
        <div className={styles.leftColumn}>
          <h2 className={styles.sectionHeader}>Summary</h2>
          <div className={styles.topContainer}>
            <QuestionsList questions={questions} />
            <GradeCard score={session.overallGrade.overallGrade} />
          </div>
          
          <h2 className={styles.sectionHeader}>Skills Breakdown</h2>
          <SkillsBreakdown scores={session.overallGrade.scores} />
          
          <h2 className={styles.sectionHeader}>Feedback</h2>
          <Feedback feedback={session.overallGrade.feedback} />

          {/* Per-question breakdowns */}
          {session.grades.map((grading, index) => (
            <QuestionBreakdown key={index} grading={grading} />
          ))}
        </div>
        
        <div className={styles.rightColumn}>
          <h2 className={styles.sectionHeader}>Video</h2>
          <Video videoUrl={session.videos[0]?.url || "No video available"} />
          
          <h2 className={styles.sectionHeader}>Transcript</h2>
          <Transcript transcript={session.transcript} />
        </div>
      </div>
    </div>
  );
}

export default SessionOverview;