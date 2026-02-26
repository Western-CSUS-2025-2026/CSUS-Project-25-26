// import { fetchAPIAuthorized } from "../fetchAuth";

type Response = "Ok" | "Error";
export async function sendRecording(
  session_comp: number,
  chunks: Blob[],
): Promise<Response> {
  const combineBlob = new Blob(chunks, { type: "video/webm" });

  const formData = new FormData();

  console.log("Len: " + chunks.length);
  formData.append("video", combineBlob, "recording.webm");
  console.log(formData.get("video"));

  // const res = await fetch(`https://api.jobless.live/video/${session_comp}`, {
  //   method: "POST",
  //   body: formData,
  //   headers: {
  //     Authorization:
  //       "RUDeYHfPoUqGeSpQcqRnHaNAhkhAHOaAbDtOqEzxWZggqPuOogoZNSrZwayicQEN",
  //   },
  // });
  const res = await fetch(`/api/video/${session_comp}`, {
    method: "POST",
    body: formData,
  });
  console.log("Video res");

  console.log(res);

  if (!res.ok) {
    console.log("Failed to upload video");
    console.log(await res.json());
    console.log(res.headers);
    return "Error";
  }

  // get the signed url
  //
  // send the video to the signed url
  return "Ok";
}
