// components/dashboard/resume-uploads-content.tsx
"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { SidebarTrigger } from "@/components/ui/sidebar"

export function ResumeUploadsContent() {
  return (
    <div className="flex flex-1 flex-col">
      <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mr-2 h-4" />
        <h1 className="text-lg font-semibold">Resume Uploads</h1>
      </header>

      <div className="flex-1 p-6 space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Upload Resumes</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="resume">Select Resume File</Label>
              <Input id="resume" type="file" accept=".pdf,.doc,.docx" />
            </div>
            <Button>Upload</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
} 