import Card from "@/components/card/card";
import LoadingText from "@/components/loadingText/loadingText";
import PastSessionsGrid from "./sessions/_components/pastSessions/pastSessions";

export default function Home() {
  return (
    <>
    {/***
       <Card height="30em" width="20em">
        <p>
          The pt size is what it is in the figma to help you decide what to use
        </p>
        <h1>Heading 1 (30 pt)</h1>
        <h2>Heading 2 (25 pt)</h2>
        <h3>Heading 3 (20 pt)</h3>
        <p>Paragraph (16 pt)</p>

        <div style={{ display: "flex", flexDirection: "row" }}>
          <LoadingText width="10em" loading presetHeight="H2">
            <h2>Test</h2>
          </LoadingText>
          <div style={{ width: "3em" }}></div>
          <LoadingText width="10em" presetHeight="H2">
            <h2>Test</h2>
          </LoadingText>
        </div>
      </Card>
    ***/}
      <div style={{ marginTop: "2rem" }}>
        <PastSessionsGrid />
      </div>
    </>
  );
}
