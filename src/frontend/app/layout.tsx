import "./globals.css";
import Link from "next/link";
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body>
    <div className="top">
      <Link href="/jobs"><strong>Queue API</strong></Link>
      <Link href="/keys">Keys</Link>
      <Link href="/jobs">Jobs</Link>
      <Link href="/dlq">Dead letter</Link>
      <Link href="/login">Account</Link>
    </div>{children}
  </body></html>);
}
