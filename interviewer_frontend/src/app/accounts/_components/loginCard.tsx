import Card from "@/components/card/card";
import styles from "./loginCard.module.css";

export default function LoginCard() {
  return (
    <div className={styles.container}>
        <Card>
        <h1 className={styles.header}>Login</h1>
        <div className={styles.coloumn}>
        <div className={styles.line}></div>

        <div className={styles.infoBox}>
        <p>Email</p>
        <input
        type="text"
        className={styles.textBox}
        placeholder="Enter your email"
        />

        <p>Password</p>
        <input
        type="password"
        className={styles.textBox}
        placeholder="Enter your password"
        />
        </div>

        <div className={styles.loginButton}>Login</div>

        <div className={styles.linkText}>
            <p>Forgot Password</p>
            <p>Sign Up</p>
        </div>

        </div>
    </Card>
    </div>
  );
}