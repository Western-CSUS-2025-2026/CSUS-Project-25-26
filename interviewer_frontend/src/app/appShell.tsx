"use client";

import { usePathname } from "next/navigation";
import SidebarProvider from "@/components/sidebar/sidebarProvider";

const HIDE_SIDEBAR_ON = ["/login", "/signup"];

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  const hideSidebar =
    HIDE_SIDEBAR_ON.includes(pathname) ||
    pathname === "/accounts" ||
    pathname.startsWith("/accounts/");

  return (
    <SidebarProvider showSidebar={!hideSidebar}>{children}</SidebarProvider>
  );
}
