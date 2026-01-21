export function fetchAPI(
  path: String,
  options: { method: string; headers: Record<string, string>; body: string },
) {
  const url = process.env.API_URL;
  if (url == undefined) {
    throw Error("ENV is not defined, API_URL must be defined as the api url");
  }
  const fullUrl = url + path;
  return fetch(fullUrl, options);
}
export function fetchAPIAuthorized(
  path: String,
  options: { method: string; headers: Record<string, string>; body: string },
) {}
