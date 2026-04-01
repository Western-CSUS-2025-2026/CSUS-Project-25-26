"use client";

import { useEffect, useRef, useState } from "react";

type MicWaveformProps = {
  enabled: boolean;
  smoothing?: number; // 0..1
};

export default function MicWaveform({
  enabled,
  smoothing = 0.85,
}: MicWaveformProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const audioCtxRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const rafRef = useRef<number | null>(null);

  const roRef = useRef<ResizeObserver | null>(null);

  const [permissionError, setPermissionError] = useState<string | null>(null);

  // canvas size helpers
  const syncCanvasSize = (canvas: HTMLCanvasElement) => {
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    if (rect.width < 2 || rect.height < 2) return;

    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.max(1, Math.floor(rect.width * dpr));
    canvas.height = Math.max(1, Math.floor(rect.height * dpr));
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0); // draw in CSS pixels
  };

  // baseline wavefrom when not recording
  const drawBaseline = (canvas: HTMLCanvasElement) => {
    syncCanvasSize(canvas);

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const w = rect.width;
    const h = rect.height;
    if (w < 2 || h < 2) return;

    const host = canvas.parentElement ?? canvas;
    const cs = getComputedStyle(host);

    const waveColor =
      cs.getPropertyValue("--wave-color").trim() || "rgba(255,255,255,0.55)";
    const fontSizePx = parseFloat(cs.fontSize) || 16;

    const thicknessEm =
      parseFloat(cs.getPropertyValue("--bar-thickness")) || 0.1;
    const gapEm = parseFloat(cs.getPropertyValue("--bar-gap")) || 0.2;

    const barW = Math.max(1, thicknessEm * fontSizePx);
    const gap = Math.max(1, gapEm * fontSizePx);

    const barCount = 36;
    const minH = h * 0.15;

    const waveformWidth = barCount * barW + (barCount - 1) * gap;
    const startX = Math.max(0, (w - waveformWidth) / 2);

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = waveColor;

    for (let i = 0; i < barCount; i++) {
      const x = startX + i * (barW + gap);
      const y = (h - minH) / 2;
      const radius = Math.min(barW / 2, 6);
      roundRect(ctx, x, y, barW, minH, radius);
      ctx.fill();
    }
  };

  // mic and audio setup
  const warmUpAudio = async () => {
    setPermissionError(null);

    // already ready
    if (audioCtxRef.current && analyserRef.current && streamRef.current) {
      if (audioCtxRef.current.state === "suspended") {
        await audioCtxRef.current.resume();
      }
      return;
    }

    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
      },
    });
    streamRef.current = stream;

    const audioCtx =
      new // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (window.AudioContext || (window as any).webkitAudioContext)();
    audioCtxRef.current = audioCtx;

    const analyser = audioCtx.createAnalyser();
    analyser.fftSize = 2048;
    analyser.smoothingTimeConstant = smoothing;
    analyserRef.current = analyser;

    const source = audioCtx.createMediaStreamSource(stream);
    source.connect(analyser);

    if (audioCtx.state === "suspended") {
      await audioCtx.resume();
    }
  };

  const startDrawing = () => {
    const canvas = canvasRef.current;
    const analyser = analyserRef.current;
    const audioCtx = audioCtxRef.current;
    if (!canvas || !analyser || !audioCtx) return;

    // cancel any previous loop
    if (rafRef.current !== null) {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    }

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const freqData = new Uint8Array(analyser.frequencyBinCount);

    const draw = () => {
      rafRef.current = requestAnimationFrame(draw);

      syncCanvasSize(canvas);

      const rect = canvas.getBoundingClientRect();
      const w = rect.width;
      const h = rect.height;
      if (w < 2 || h < 2) return;

      ctx.clearRect(0, 0, w, h);
      analyser.getByteFrequencyData(freqData);

      const host = canvas.parentElement ?? canvas;
      const cs = getComputedStyle(host);

      const waveColor =
        cs.getPropertyValue("--wave-color").trim() || "rgba(255,255,255,0.55)";
      const fontSizePx = parseFloat(cs.fontSize) || 16;

      const thicknessEm =
        parseFloat(cs.getPropertyValue("--bar-thickness")) || 0.1;
      const gapEm = parseFloat(cs.getPropertyValue("--bar-gap")) || 0.2;

      const barW = Math.max(1, thicknessEm * fontSizePx);
      const gap = Math.max(1, gapEm * fontSizePx);

      const barCount = 36;

      const waveformWidth = barCount * barW + (barCount - 1) * gap;
      const startX = Math.max(0, (w - waveformWidth) / 2);

      const minH = h * 0.15;
      const gate = 0.02;
      const maxExtra = h - minH;

      // speech bands: ~80Hz to ~8kHz
      const nyquist = audioCtx.sampleRate / 2;
      const minFreq = 80;
      const maxFreq = Math.min(8000, nyquist);

      const minBin = Math.floor((minFreq / nyquist) * (freqData.length - 1));
      const maxBin = Math.max(
        minBin + 1,
        Math.floor((maxFreq / nyquist) * (freqData.length - 1)),
      );

      const usableBins = maxBin - minBin + 1;
      const bandSize = Math.max(3, Math.floor(usableBins / barCount));

      ctx.fillStyle = waveColor;

      for (let i = 0; i < barCount; i++) {
        const t = barCount <= 1 ? 0 : i / (barCount - 1);

        const startBin = Math.floor(minBin + t * (usableBins - bandSize));
        const endBin = Math.min(maxBin + 1, startBin + bandSize);

        let sum = 0;
        for (let b = startBin; b < endBin; b++) sum += freqData[b];

        let level = sum / Math.max(1, endBin - startBin) / 255;

        level = level < gate ? 0 : (level - gate) / (1 - gate);
        level = Math.pow(level, 0.55);

        const barH = minH + level * maxExtra;

        const x = startX + i * (barW + gap);
        const y = (h - barH) / 2;

        const radius = Math.min(barW / 2, 6);
        roundRect(ctx, x, y, barW, barH, radius);
        ctx.fill();
      }
    };

    draw();
  };

  const pauseDrawing = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    if (rafRef.current !== null) {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    }

    drawBaseline(canvas);
  };

  // setup baseline and resize observer
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    // draw baseline after layout settles
    requestAnimationFrame(() => drawBaseline(canvas));

    // keep baseline consistent on resize
    const host = canvas.parentElement ?? canvas;
    roRef.current?.disconnect();
    roRef.current = new ResizeObserver(() => {
      if (!enabled) drawBaseline(canvas);
      else syncCanvasSize(canvas);
    });
    roRef.current.observe(host);

    return () => {
      roRef.current?.disconnect();
      roRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // run once

  // Main toggle: enabled -> warmUp + draw, disabled -> pause
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    if (enabled) {
      void (async () => {
        try {
          await warmUpAudio();
          startDrawing();
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (e: any) {
          setPermissionError(
            e?.name === "NotAllowedError"
              ? "Mic permission denied."
              : "Could not access microphone.",
          );
          pauseDrawing();
        }
      })();
    } else {
      pauseDrawing();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [enabled, smoothing]);

  // cleanup on unmount
  // stop tracks + close audio context
  useEffect(() => {
    return () => {
      if (rafRef.current !== null) {
        cancelAnimationFrame(rafRef.current);
        rafRef.current = null;
      }

      if (streamRef.current) {
        streamRef.current.getTracks().forEach((t) => t.stop());
        streamRef.current = null;
      }

      if (audioCtxRef.current) {
        try {
          void audioCtxRef.current.close();
        } catch {}
        audioCtxRef.current = null;
      }

      analyserRef.current = null;
    };
  }, []);

  return (
    <>
      <canvas
        ref={canvasRef}
        style={{ width: "100%", height: "100%", display: "block" }}
        aria-hidden="true"
      />
      {permissionError && (
        <p style={{ fontSize: 12, opacity: 0.7, margin: 0 }}>
          {permissionError}
        </p>
      )}
    </>
  );
}

function roundRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  r: number,
) {
  const radius = Math.max(0, Math.min(r, w / 2, h / 2));
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.arcTo(x + w, y, x + w, y + h, radius);
  ctx.arcTo(x + w, y + h, x, y + h, radius);
  ctx.arcTo(x, y + h, x, y, radius);
  ctx.arcTo(x, y, x + w, y, radius);
  ctx.closePath();
}
