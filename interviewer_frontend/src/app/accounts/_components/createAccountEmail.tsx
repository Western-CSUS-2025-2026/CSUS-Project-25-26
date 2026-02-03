import Card from "@/components/card/card";
import styles from "./loginCard.module.css";

interface CreateAccountEmailCardProps {
  onNext: () => void;
  onBackToLogin: () => void;
}

export default function CreateAccountEmailCard({
  onNext,
  onBackToLogin,
}: CreateAccountEmailCardProps) {
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
                  <p>Email</p>
                  <input
                    type="email"
                    className={styles.textBox}
                    placeholder="Enter your email"
                    autoComplete="email"
                  />
                </div>

                <div className={styles.blankSpace}></div>

                <button
                  className={styles.loginButton}
                  type="button"
                  onClick={onNext}
                >
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
