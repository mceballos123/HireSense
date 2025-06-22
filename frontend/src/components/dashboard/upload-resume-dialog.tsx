"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Loader2, Upload, FileText, XCircle } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

interface JobPost {
  id: string
  title: string
  summary: string
  description: string
}

interface UploadResumeDialogProps {
  job: JobPost | null
  open: boolean
  onOpenChange: (open: boolean) => void
  onUploadStart: () => void
  onUploadComplete: (result: any) => void
}

export function UploadResumeDialog({
  job,
  open,
  onOpenChange,
  onUploadStart,
  onUploadComplete,
}: UploadResumeDialogProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [candidateName, setCandidateName] = useState<string>("")
  const [isUploading, setIsUploading] = useState<boolean>(false)
  const [error, setError] = useState<string>("")

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      const allowedTypes = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      ]
      if (!allowedTypes.includes(file.type)) {
        setError("Please select a PDF, DOC, or DOCX file.")
        setSelectedFile(null)
        return
      }

      if (file.size > 10 * 1024 * 1024) {
        setError("File size must be less than 10MB.")
        setSelectedFile(null)
        return
      }

      setSelectedFile(file)
      setError("")
    }
  }

  const handleUpload = async () => {
    if (!selectedFile || !candidateName.trim() || !job) {
      setError("Please select a file and enter the candidate's name.")
      return
    }

    onUploadStart()
    setIsUploading(true)
    setError("")

    try {
      const formData = new FormData()
      formData.append("resume_file", selectedFile)
      formData.append("candidate_name", candidateName.trim())
      formData.append("job_title", job.title)
      formData.append("job_description", job.description || job.summary)

      const response = await fetch("http://localhost:8080/evaluate-candidate", {
        method: "POST",
        body: formData,
      })

      const result = await response.json()

      if (response.ok) {
        onUploadComplete(result)
        handleClose()
      } else {
        setError(result.error || result.detail || "Upload failed.")
      }
    } catch (err) {
      setError("Network error: Could not connect to the server.")
      console.error("Upload error:", err)
    } finally {
      setIsUploading(false)
    }
  }

  const handleClose = () => {
    setSelectedFile(null)
    setCandidateName("")
    setError("")
    setIsUploading(false)
    onOpenChange(false)
  }

  if (!job) return null

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Upload Resume for {job.title}</DialogTitle>
          <DialogDescription>
            Submit a candidate's resume for analysis against this job post.
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="candidate-name">Candidate Name</Label>
            <Input
              id="candidate-name"
              type="text"
              placeholder="Enter candidate's full name"
              value={candidateName}
              onChange={(e) => setCandidateName(e.target.value)}
              disabled={isUploading}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="resume">Resume File</Label>
            <Input
              id="resume"
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={handleFileChange}
              disabled={isUploading}
            />
            {selectedFile && (
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <FileText className="h-4 w-4" />
                <span>{selectedFile.name}</span>
                <span className="text-xs">
                  ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                </span>
              </div>
            )}
          </div>
          {error && (
            <Alert variant="destructive">
              <XCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={handleClose} disabled={isUploading}>
            Cancel
          </Button>
          <Button
            onClick={handleUpload}
            disabled={!selectedFile || !candidateName.trim() || isUploading}
          >
            {isUploading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Upload className="mr-2 h-4 w-4" />
                Upload & Analyze
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
} 
 