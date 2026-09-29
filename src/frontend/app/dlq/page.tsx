"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
type Job = { id: string; kind: string; error: string; attempts: number };
export default function DlqPage() {
  const [rows, setRows] = useState<Job[]>([]);
  useEffect(() => { api<Job[]>("/jobs?status=dead").then(setRows).catch(() => null); }, []);
  return (
    <main>
      <h1>Dead letter</h1>
      {rows.map((j) => <article className="card" key={j.id}>{j.kind} failed {j.attempts}× — {j.error}</article>)}
    </main>
  );
}
