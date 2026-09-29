"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
type Key = { id: string; name: string; prefix: string; revoked: boolean; token?: string };
export default function KeysPage() {
  const [rows, setRows] = useState<Key[]>([]);
  const [fresh, setFresh] = useState("");
  const [error, setError] = useState("");
  async function load() { setRows(await api<Key[]>("/keys")); }
  useEffect(() => { load().catch((err: Error) => setError(err.message)); }, []);
  return (
    <main>
      <h1>API keys</h1>
      {error ? <p className="err">{error}</p> : null}
      <button type="button" onClick={() => api<Key>("/keys", { method: "POST", body: JSON.stringify({ name: "console" }) }).then((k) => { setFresh(k.token ?? ""); return load(); })}>Issue key</button>
      {fresh ? <p className="card">Copy now: <code>{fresh}</code></p> : null}
      {rows.map((k) => <article className="card" key={k.id}>{k.name} · {k.prefix}… {k.revoked ? "revoked" : "live"}</article>)}
    </main>
  );
}
