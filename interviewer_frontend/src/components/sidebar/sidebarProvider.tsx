import styles from "./sidebar.module.css";
import Sidebar from "./sidebar";

interface SidebarProviderProps {
  children?: React.ReactNode;
}
function SidebarProvider(props: SidebarProviderProps) {
  return (
    <div className={styles.sidebarProvider}>
      <Sidebar></Sidebar>
      <div className={styles.mainContent}>{props.children}</div>
    </div>
  );
}
export default SidebarProvider;
