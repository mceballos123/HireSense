// components/dashboard/resume-uploads-content.tsx
"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Loader2, Upload, FileText, CheckCircle, XCircle } from "lucide-react"

interface UploadResult {
  candidate_name: string
  skills: string[]
  experience_years: number
  experience_level: string
  key_achievements: string[]
  analysis: string
  status: string
}

export function ResumeUploadsContent() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [candidateName, setCandidateName] = useState<string>("")
  const [isUploading, setIsUploading] = useState<boolean>(false)
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null)
  const [error, setError] = useState<string>("")

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      // Validate file type
      const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
      if (!allowedTypes.includes(file.type)) {
        setError("Please select a PDF, DOC, or DOCX file")
        setSelectedFile(null)
        return
      }
      
      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError("File size must be less than 10MB")
        setSelectedFile(null)
        return
      }
      
      setSelectedFile(file)
      setError("")
      setUploadResult(null)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile || !candidateName.trim()) {
      setError("Please select a file and enter candidate name")
      return
    }

    setIsUploading(true)
    setError("")
    
    try {
      const formData = new FormData()
      formData.append('file', selectedFile)
      formData.append('candidate_name', candidateName.trim())

      const response = await fetch('http://localhost:8080/upload-resume', {
        method: 'POST',
        body: formData,
      })

      const result = await response.json()

      if (response.ok) {
        setUploadResult(result as UploadResult)
        // Clear form on success
        setSelectedFile(null)
        setCandidateName("")
        // Reset file input
        const fileInput = document.getElementById('resume') as HTMLInputElement
        if (fileInput) fileInput.value = ''
      } else {
        setError(result.error || result.detail || 'Upload failed')
      }
    } catch (err) {
      setError('Network error: Could not connect to server')
      console.error('Upload error:', err)
    } finally {
      setIsUploading(false)
    }
  }

  const resetResults = () => {
    setUploadResult(null)
    setError("")
  }

  return (
    <div className="flex flex-1 flex-col">
      <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
        <h1 className="text-lg font-semibold">Resume Uploads</h1>
      </header>

      <div className="flex-1 p-6 space-y-6">
        {/* Upload Form */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-5 w-5" />
              Upload Resume
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
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
              <Label htmlFor="resume">Select Resume File</Label>
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
                  <span>({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)</span>
                </div>
              )}
            </div>

            {error && (
              <Alert variant="destructive">
                <XCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="flex gap-2">
              <Button 
                onClick={handleUpload} 
                disabled={!selectedFile || !candidateName.trim() || isUploading}
                className="flex items-center gap-2"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Upload className="h-4 w-4" />
                    Upload & Analyze
                  </>
                )}
              </Button>
              
              {uploadResult && (
                <Button variant="outline" onClick={resetResults}>
                  Upload Another
                </Button>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Results Display */}
        {uploadResult && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-green-600" />
                Analysis Results for {uploadResult.candidate_name}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label className="text-sm font-medium">Experience Level</Label>
                  <div className="mt-1">
                    <Badge variant="secondary">{uploadResult.experience_level}</Badge>
                  </div>
                </div>
                
                <div>
                  <Label className="text-sm font-medium">Years of Experience</Label>
                  <div className="mt-1">
                    <Badge variant="outline">{uploadResult.experience_years} years</Badge>
                  </div>
                </div>
              </div>

              <div>
                <Label className="text-sm font-medium">Technical Skills</Label>
                <div className="mt-2 flex flex-wrap gap-2">
                  {uploadResult.skills.map((skill, index) => (
                    <Badge key={index} variant="default">{skill}</Badge>
                  ))}
                </div>
              </div>

              <div>
                <Label className="text-sm font-medium">Key Achievements</Label>
                <ul className="mt-2 space-y-1">
                  {uploadResult.key_achievements.map((achievement, index) => (
                    <li key={index} className="text-sm text-muted-foreground flex items-start gap-2">
                      <span className="text-green-600 mt-1">•</span>
                      {achievement}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <Label className="text-sm font-medium">Analysis Summary</Label>
                <p className="mt-2 text-sm text-muted-foreground bg-muted p-3 rounded-md">
                  {uploadResult.analysis}
                </p>
              </div>

              {uploadResult.status && (
                <div className="flex items-center gap-2 text-sm">
                  <Badge 
                    variant={uploadResult.status === 'success' ? 'default' : 'secondary'}
                  >
                    Status: {uploadResult.status}
                  </Badge>
                </div>
              )}
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
} 