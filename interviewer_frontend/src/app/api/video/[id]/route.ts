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
  headers.set("Authorization", `${token?.value}`);
  headers.set(
    "Content-Disposition",
    'form-data; name="video"; filename="video.webm"',
  );
  console.log(headers);

  const res = await fetch(url + `video/${id}`, {
    method: "POST",
    headers: headers,
    body: req.body,
    duplex: "half",
  });
  console.log(res);
  const body = await res.json();
  console.log(body);

  return Response.json({ success: res.ok, body: body });
}
