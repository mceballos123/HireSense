"use client"

import { useState, useCallback } from "react"
import { useDropzone } from "react-dropzone"
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
import { Loader2, UploadCloud, FileText, X, CheckCircle } from "lucide-react"
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

  const onDrop = useCallback((acceptedFiles: File[], fileRejections: any[]) => {
    setError("")
    if (fileRejections.length > 0) {
      const firstError = fileRejections[0].errors[0]
      if (firstError.code === "file-too-large") {
        setError("File is larger than 10MB.")
      } else if (firstError.code === "file-invalid-type") {
        setError("Invalid file type. Please upload a PDF, DOC, or DOCX.")
      } else {
        setError(firstError.message)
      }
      setSelectedFile(null)
    } else if (acceptedFiles.length > 0) {
      setSelectedFile(acceptedFiles[0])
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/msword": [".doc"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
        ".docx",
      ],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: false,
  })

  const handleUpload = async () => {
    if (!selectedFile || !candidateName.trim() || !job) {
      setError("Please add a resume file and enter the candidate's name.")
      return
    }

    onUploadStart()
    setIsUploading(true)
    setError("")

    try {
      const formData = new FormData()
      formData.append("file", selectedFile)
      formData.append("candidate_name", candidateName.trim())
      formData.append("job_title", job.title)

      const response = await fetch("http://localhost:8080/upload-resume", {
        method: "POST",
        body: formData,
      })

      const result = await response.json()

      if (response.ok) {
        onUploadComplete(result)
        handleClose()
      } else {
        setError(result.error || result.detail || "Upload failed.")
        setIsUploading(false)
      }
    } catch (err) {
      setError("Network error: Could not connect to the server.")
      console.error("Upload error:", err)
      setIsUploading(false)
    }
  }
  
  const removeFile = () => {
    setSelectedFile(null)
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
      <DialogContent className="sm:max-w-[525px] bg-white dark:bg-slate-900/95 dark:backdrop-blur-sm">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold bg-gradient-to-r from-slate-900 via-blue-800 to-violet-800 bg-clip-text text-transparent dark:from-white dark:via-blue-200 dark:to-violet-200">
            Upload Resume for {job.title}
          </DialogTitle>
          <DialogDescription>
            Submit a candidate's resume for analysis against this job post.
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-6 py-4">
          <div className="space-y-2">
            <Label htmlFor="candidate-name" className="font-semibold">Candidate Name</Label>
            <Input
              id="candidate-name"
              type="text"
              placeholder="Enter candidate's full name"
              value={candidateName}
              onChange={(e) => setCandidateName(e.target.value)}
              disabled={isUploading}
              className="h-11"
            />
          </div>
          
          <div className="space-y-2">
            <Label className="font-semibold">Resume File</Label>
            {selectedFile ? (
              <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-200 dark:bg-slate-800 dark:border-slate-700">
                <div className="flex items-center gap-3">
                  <FileText className="h-6 w-6 text-blue-500" />
                  <div className="text-sm">
                    <p className="font-semibold text-slate-800 dark:text-slate-200">{selectedFile.name}</p>
                    <p className="text-slate-500 dark:text-slate-400">
                      {(selectedFile.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                </div>
                <Button
                  size="icon"
                  variant="ghost"
                  onClick={removeFile}
                  disabled={isUploading}
                  className="h-8 w-8 rounded-full hover:bg-red-100 dark:hover:bg-red-900/50"
                >
                  <X className="h-4 w-4 text-slate-500 hover:text-red-600 dark:hover:text-red-500" />
                </Button>
              </div>
            ) : (
              <div
                {...getRootProps()}
                className={`relative flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg cursor-pointer transition-colors
                  ${isDragActive ? "border-blue-500 bg-blue-50 dark:bg-blue-900/30" : "border-slate-300 dark:border-slate-700 hover:border-blue-400 dark:hover:border-blue-600"}
                `}
              >
                <input {...getInputProps()} />
                <UploadCloud className="h-10 w-10 text-slate-400 dark:text-slate-500 mb-3" />
                <p className="text-slate-600 dark:text-slate-400 text-center">
                  <span className="font-semibold text-blue-600 dark:text-blue-400">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-slate-500 dark:text-slate-500 mt-1">
                  PDF, DOC, DOCX (max 10MB)
                </p>
              </div>
            )}
          </div>

          {error && (
            <Alert variant="destructive">
              <X className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </div>
        <DialogFooter className="gap-2 sm:gap-4">
          <Button
            variant="outline"
            onClick={handleClose}
            disabled={isUploading}
            className="h-10 disabled:border-slate-200 disabled:text-slate-400 dark:disabled:border-slate-800 dark:disabled:text-slate-500"
          >
            Cancel
          </Button>
          <Button
            onClick={handleUpload}
            disabled={!selectedFile || !candidateName.trim() || isUploading}
            className="h-10 w-40 bg-slate-900 text-white hover:bg-slate-800 dark:bg-slate-50 dark:text-slate-900 dark:hover:bg-slate-200 disabled:bg-slate-200 disabled:text-slate-500 dark:disabled:bg-slate-800 dark:disabled:text-slate-400"
          >
            {isUploading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <UploadCloud className="mr-2 h-4 w-4" />
                Upload & Analyze
              </>
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
} 
 