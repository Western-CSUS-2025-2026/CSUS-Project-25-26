import styles from "./sidebar.module.css";
import Sidebar from "./sidebar";

interface SidebarProviderProps {
  children?: React.ReactNode;
  showSidebar?: boolean;
}

function SidebarProvider({
  children,
  showSidebar = true,
}: SidebarProviderProps) {
  return (
    <div className={styles.sidebarProvider}>
      {showSidebar && <Sidebar />}
      <div className={styles.mainContent}>{children}</div>
    </div>
  );
}

export default SidebarProvider;
