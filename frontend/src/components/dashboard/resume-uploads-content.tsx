"use client"

import { Upload } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { SidebarTrigger } from "@/components/ui/sidebar"

export function ResumeUploadsContent() {
  return (
    <div className="flex flex-1 flex-col bg-gradient-to-br from-slate-50 via-white to-blue-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-blue-950/20">
      <header className="flex h-20 items-center gap-3 border-b border-white/20 bg-white/70 backdrop-blur-xl px-8 shadow-sm dark:bg-slate-900/70 dark:border-slate-800/50">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mr-3 h-6" />
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-violet-600">
            <Upload className="h-4 w-4 text-white" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 via-blue-800 to-violet-800 bg-clip-text text-transparent dark:from-white dark:via-blue-200 dark:to-violet-200">
            Resume Uploads
          </h1>
        </div>
      </header>

      <div className="flex-1 flex items-center justify-center p-8">
        <Card className="w-full max-w-md border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-lg dark:bg-slate-800/90 dark:border-slate-700/60">
          <CardHeader className="text-center pb-6">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-blue-600 to-violet-600">
              <Upload className="h-8 w-8 text-white" />
            </div>
            <CardTitle className="text-2xl font-bold text-slate-900 dark:text-white">Upload Resume</CardTitle>
            <p className="text-slate-600 dark:text-slate-400">Upload candidate resumes for AI analysis</p>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="resume" className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Select Resume File
              </Label>
              <Input 
                id="resume" 
                type="file" 
                accept=".pdf,.doc,.docx" 
                className="file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-gradient-to-r file:from-blue-600 file:to-violet-600 file:text-white hover:file:from-blue-700 hover:file:to-violet-700 file:cursor-pointer"
              />
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Supported formats: PDF, DOC, DOCX (Max 10MB)
              </p>
            </div>
            <Button className="w-full bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 text-white border-0 shadow-lg shadow-blue-500/25 py-3">
              <Upload className="h-4 w-4 mr-2" />
              Upload Resume
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
} 