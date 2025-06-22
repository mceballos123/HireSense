import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { AppSidebar } from "@/components/ui/sidebar"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "AI Recruiter Dashboard",
  description: "AI-powered resume evaluation system for recruiters",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-foreground">
        <AppSidebar />
        <main className="ml-[100px] p-8">{children}</main>
      </body>
    </html>
  )
}


