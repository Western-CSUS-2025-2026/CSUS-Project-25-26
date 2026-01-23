import Card from "@/components/card/card";
import styles from "./loginCard.module.css";


interface LoginCardProps {
  onSignUp: () => void;
}

export default function LoginCard({ onSignUp }: LoginCardProps) {
  return (    
    <>
      <div className={styles.container}>
        {/* wrapper class */}
        <div className="loginCardRadiusOverride">
        <div className={styles.sizeBox}>
          <Card fillHeight fillWidth>
            <h1 className={styles.header}>Login</h1>

            <div className={styles.coloumn}>
              <div className={styles.line}></div>

              <div className={styles.infoBox}>
                <p>Email</p>
                <input
                  type="text"
                  className={styles.textBox}
                  placeholder="Enter your email"
                  autoComplete="email"
                />

                <p>Password</p>
                <input
                  type="password"
                  className={styles.textBox}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                />
              </div>

              <button className={styles.loginButton} type="button">Login</button>

            <div className={styles.linkText}>
            <button type="button" className={styles.linkButton}>
                Forgot Password
            </button>
           <button type="button" onClick={onSignUp} className={styles.linkButton}>
                Sign Up
            </button>
            </div>

            </div>
          </Card>
        </div>
      </div>
      </div>

      {/*change card border radius*/}
      <style>{`
        .loginCardRadiusOverride .cardStyle {
          border-radius: 2em !important;
        }
      `}</style>
    </>
  );
}
