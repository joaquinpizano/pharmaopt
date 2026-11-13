import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PharmaOpt | Evidence-led review intelligence",
  description:
    "A transparent research interface for prioritizing historical pharmaceutical package review.",
  applicationName: "PharmaOpt",
  icons: {
    icon: "/icon.svg",
    apple: "/logo-mark.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
