"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
type Job = { id: string; kind: string; status: string; attempts: number; result: string; error: string };
export default function JobsPage() {
  const [rows, setRows] = useState<Job[]>([]);
  const [kind, setKind] = useState("echo");
  const [text, setText] = useState("hello");
  const [error, setError] = useState("");
  async function load() { setRows(await api<Job[]>("/jobs")); }
  useEffect(() => { load().catch((err: Error) => setError(err.message)); }, []);
  return (
    <main>
      <h1>Jobs</h1>
      {error ? <p className="err">{error}</p> : null}
      <p>
        <select value={kind} onChange={(e) => setKind(e.target.value)}><option>echo</option><option>upper</option><option>fail</option></select>
        <input value={text} onChange={(e) => setText(e.target.value)} />
        <button type="button" onClick={() => api("/jobs", { method: "POST", body: JSON.stringify({ kind, payload: { text, message: text } }) }).then(load)}>Enqueue</button>
        <button type="button" onClick={() => api("/worker/tick", { method: "POST" }).then(load)}>Tick worker</button>
      </p>
      {rows.map((j) => <article className="card" key={j.id}><strong>{j.status}</strong> {j.kind} · tries {j.attempts}<p className="muted">{j.result || j.error || "waiting"}</p></article>)}
    </main>
  );
}
