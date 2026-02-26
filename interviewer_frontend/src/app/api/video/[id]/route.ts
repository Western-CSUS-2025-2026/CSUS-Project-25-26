import { cookies } from "next/headers";

export async function POST(
  req: Request,
  { params }: { params: { id: string } },
) {
  const { id } = await params;

  const token = (await cookies()).get("session_token");

  if (process.env.API_URL == undefined) {
    throw new Error("API_URL is not set, please set it in a .env file");
  }
  const url = process.env.API_URL;

  const headers = new Headers(req.headers);

  headers.delete("Host");
  return fetch(url + `/video/${id}`, {
    method: "POST",
    headers: {
      Authorization: `${token?.value}`,
      ...headers,
    },
    body: req.body,
    duplex: "half",
  });
}
