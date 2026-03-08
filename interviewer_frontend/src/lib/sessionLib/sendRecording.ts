"use server";
import { fetchAPIAuthorized } from "../fetchAuth";

type Response = "Ok" | "Error";
export async function sendRecording(
  session_comp: number,
  chunks: Blob,
): Promise<Response> {
  const combineBlob = chunks;

  const res = await fetchAPIAuthorized(`video/${session_comp}/upload-url`, {
    method: "GET",
  });

  if (!res.success) {
    console.log(res);
    return "Error";
  }

  console.log("Size: " + combineBlob.size);
  const video_res = await fetch(res.body.url, {
    method: "PUT",
    headers: {
      "Content-Type": "video/webm",
    },
    body: combineBlob,
  });

  if (!video_res.ok) {
    console.log(video_res);
    return "Error";
  }
  console.log("Completed Video upload");

  // get the signed url
  //
  // send the video to the signed url
  return "Ok";
}
