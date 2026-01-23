import Card from "@/components/card/card";
import styles from "./loginCard.module.css";

interface CreateAccountCardProps {
  onBackToLogin: () => void;
}

export default function CreateAccountCard({ onBackToLogin }: CreateAccountCardProps) {
  return (
    <>
      <div className={styles.container}>
        <div className="loginCardRadiusOverride">
          <div className={styles.sizeBox}>
            <Card fillHeight fillWidth>
              <h1 className={styles.header}>Create Account</h1>

              <div className={styles.coloumn}>
                <div className={styles.line}></div>

                <div className={styles.infoBox}>
                  <p>First Name</p>
                  <input
                    type="text"
                    className={styles.textBox}
                    placeholder="Enter your first name"
                    autoComplete="given-name"
                  />

                  <p>Last Name</p>
                  <input
                    type="text"
                    className={styles.textBox}
                    placeholder="Enter your last name"
                    autoComplete="family-name"
                  />
                </div>

                <button className={styles.loginButton} type="button">
                  Next
                </button>

                <div>
                  <button
                    type="button"
                    className={styles.linkButton}
                    onClick={onBackToLogin}
                  >
                    Back
                  </button>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>

      <style>{`
        .loginCardRadiusOverride .cardStyle {
          border-radius: 2em !important;
        }
      `}</style>
    </>
  );
}
