export function convertToLetterGrade(score: number): string {
  if (score >= 0.97) return "A+";
  if (score >= 0.93) return "A";
  if (score >= 0.90) return "A-";
  if (score >= 0.87) return "B+";
  if (score >= 0.83) return "B";
  if (score >= 0.80) return "B-";
  if (score >= 0.77) return "C+";
  if (score >= 0.73) return "C";
  if (score >= 0.70) return "C-";
  if (score >= 0.60) return "D";
  return "F";
}

