import { useEffect, useRef, useState } from "react";
type Callback = { callback: (elapsed: number) => void; duration: number };

export function useTimer() {
  const [running, setRunning] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [callbacks, setCallbacks] = useState<Callback[]>([]);

  const startRef = useRef(0);
  const intervalRef = useRef<NodeJS.Timeout>(null);
  const addCallback = (
    callback: (elapsed: number) => void,
    duration: number,
  ) => {
    setCallbacks((prev) =>
      prev.concat({ callback: callback, duration: duration }),
    );
  };

  useEffect(() => {
    if (!running) return;

    startRef.current = Date.now() - elapsed;

    const inter = setInterval(() => {
      const elapsed = Date.now() - startRef.current;
      setElapsed(elapsed);

      setCallbacks((prev) => {
        return prev.filter((callback) => {
          if (callback.duration < elapsed) {
            return false;
          }
          return true;
        });
      });

      callbacks.forEach((callback) => {
        if (callback.duration < elapsed) {
          callback.callback(elapsed);
        }
      });
    }, 100);
    intervalRef.current = inter;

    return () => clearInterval(intervalRef.current!);
  }, [running, callbacks, startRef, intervalRef, elapsed]);

  const start = (fromZero = false) => {
    const now = Date.now();

    startRef.current = fromZero ? now : now - elapsed;
    setElapsed(fromZero ? 0 : elapsed);
    setRunning(true);
  };

  return {
    elapsed,
    running,
    start: start,
    pause: () => setRunning(false),
    reset: () => {
      setElapsed(0);
      setRunning(false);
      startRef.current = 0;
      clearInterval(intervalRef.current!);
    },
    addCallback: addCallback,
  };
}
