import { Suspense } from "react";

// use @lib/getSessionById to fetch the session
function GradeOverview() {
  return (
    <Suspense fallback={"Loading State here"}>
      {/* Component goes in here*/}
    </Suspense>
  );
}

export default GradeOverview;
