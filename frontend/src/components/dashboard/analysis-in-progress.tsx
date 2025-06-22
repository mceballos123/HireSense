"use client"

import { Loader2 } from "lucide-react"

export function AnalysisInProgress() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center text-center bg-gradient-to-br from-slate-50 via-white to-blue-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-blue-950/20">
      <div className="space-y-4">
        <Loader2 className="mx-auto h-16 w-16 animate-spin text-blue-600" />
        <h2 className="text-3xl font-bold bg-gradient-to-r from-slate-900 via-blue-800 to-violet-800 bg-clip-text text-transparent dark:from-white dark:via-blue-200 dark:to-violet-200">
          Analysis in Progress
        </h2>
        <p className="text-slate-600 dark:text-slate-400 max-w-md">
          Our team of AI agents is currently evaluating the candidate's resume against the job description. This may take a moment.
        </p>
      </div>
    </div>
  )
} 