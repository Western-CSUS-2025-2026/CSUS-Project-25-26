
'use client';

import { useEffect, useState } from "react";
import { getPastSessions } from "@/lib/pastSessions";
import Card from "@/components/card/card";
import styles from "./pastSessions.module.css";
import { SimpleSession } from "@/types/simpleSession";

export default function PastSessionsGrid() {
	const [sessions, setSessions] = useState<SimpleSession[]>([]);

	useEffect(() => {
		const loadSessions = async () => {
			const data = await getPastSessions();
			setSessions(data);
		};
		loadSessions();
	}, []);

	return (
		<div className={styles.grid}>
			{sessions.map((session, idx) => (
				<Card key={idx} fillWidth>
					<div className={styles.cardInner}>
						<div className={styles.title}>{session.title}</div>

						{session.state === "PROCESSING" ? (
							<div className={styles.processing}>
								<div className={styles.status}>Processing...</div>
								<div className={styles.spinner} />
							</div>
						) : (
							<div className={styles.completed}>
								<div className={styles.details}>
									<span className={styles.grade}>
										{"overallGrade" in session ? (session.overallGrade.overallGrade * 100).toFixed(0) + "%" : "-"}
									</span>
									<span className={styles.date}>{new Date(session.createTime).toLocaleDateString()}</span>
								</div>
							</div>
						)}
					</div>
				</Card>
			))}
		</div>
	);
}
