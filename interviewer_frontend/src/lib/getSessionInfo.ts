interface GetSessionInfoReturn {
  questions: string[];
}
export async function getSessionInfo(): Promise<GetSessionInfoReturn> {
  return {
    questions: [
      "What is your favourite color?",
      "How tall are you?",
      "What is something your good at?",
    ],
  };
}
