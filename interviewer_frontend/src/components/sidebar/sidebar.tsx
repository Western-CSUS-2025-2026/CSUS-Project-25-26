"use client";

import styles from "./sidebar.module.css";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import Image from "next/image";

function Sidebar() {
  const iconHeight = 12;
  const router = useRouter();

  const logOut = () => {
    router.push("/accounts");
  };
  return (
    <div className={styles.sidebar}>
      {/* User Profile Section */}
      <div className={styles.userProfile}>
        <div className={styles.avatar}></div>
        <span className={styles.userName}></span>
      </div>

      {/* Navigation Buttons */}
      <nav className={styles.navigation}>
        <NavButton href="/home" label="Home" icon="/icons/home.svg" />
        <NavButton
          href="/sessions"
          label="Sessions"
          icon="/icons/sessions.svg"
        />
        <NavButton
          href="/settings"
          label="Settings"
          icon="/icons/settings.svg"
        />
      </nav>

      {/* Bottom Section */}
      <div className={styles.bottomSection}>
        <button className={styles.helpButton}>
          <Image
            src="/icons/help.svg"
            alt="Help"
            width={iconHeight}
            height={iconHeight}
          />
          <span>Help</span>
        </button>
        <button className={styles.logoutButton} onClick={logOut}>
          <Image
            src="/icons/logout.svg"
            alt="Logout"
            width={iconHeight * 1.2}
            height={iconHeight}
          />
          <span className={styles.logoutText}>Logout</span>
        </button>
        <p className={styles.credit}>
          Credit to CSUS
          <br />
          2025-2026
        </p>
      </div>
    </div>
  );
}

// Navigation Button Component
function NavButton({
  href,
  label,
  icon,
}: {
  href: string;
  label: string;
  icon: string;
}) {
  const pathname = usePathname();
  const isActive = pathname === href;

  return (
    <Link
      href={href}
      className={`${styles.navButton} ${isActive ? styles.active : ""}`}
    >
      <Image src={icon} alt={label} width={20} height={20} />
      <span>{label}</span>
    </Link>
  );
}

export default Sidebar;
