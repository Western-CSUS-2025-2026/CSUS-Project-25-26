export function fetchAPI(
  path: string,
  options: { method: string; headers: Record<string, string>; body?: string },
) {
  const base = process.env.API_URL;
  if (!base) {
    throw new Error("API_URL is not defined");
  }

  // make sure one slash between base and path
  const fullUrl =
    base.replace(/\/$/, "") + "/" + path.toString().replace(/^\//, "");

  return fetch(fullUrl, options);
}
