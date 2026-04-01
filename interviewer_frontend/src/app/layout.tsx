import type { Metadata } from "next";
import "./globals.css";
import AppShell from "./appShell";
import { SafariWarningNoSSR } from "@/components/safariWarning/safariWarning";

export const metadata: Metadata = {
  title: "Jobless.ai",
  description: "Ai behavioural interview prep",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <AppShell>{children}</AppShell>
        <SafariWarningNoSSR></SafariWarningNoSSR>
      </body>
    </html>
  );
}
