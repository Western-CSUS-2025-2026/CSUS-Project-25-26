import LoadingSpinner from "@/components/loadingSpinner/loadingSpinner";

export default function Loading() {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        width: "calc(100vw - 22vw)",
      }}
    >
      <LoadingSpinner />
    </div>
  );
}
