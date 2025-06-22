"use client"

import { ArrowLeft, Download, Mail, Phone } from "lucide-react"
import Link from "next/link"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"
import { SidebarTrigger } from "@/components/ui/sidebar"

// Mock detailed applicant data
const getApplicantData = (id: string) => {
  const applicants = {
    "1": {
      name: "Sarah Johnson",
      email: "sarah.johnson@email.com",
      phone: "+1 (555) 123-4567",
      position: "Senior Frontend Developer",
      overallScore: 92,
      skills: [
        { name: "React", score: 95, required: true },
        { name: "TypeScript", score: 90, required: true },
        { name: "JavaScript", score: 95, required: true },
        { name: "CSS/SCSS", score: 88, required: false },
        { name: "Node.js", score: 75, required: false },
        { name: "Testing", score: 85, required: true },
      ],
      experience: "5+ years",
      education: "BS Computer Science",
      summary:
        "Highly skilled frontend developer with extensive React and TypeScript experience. Strong portfolio showcasing responsive web applications and modern development practices.",
      strengths: [
        "Excellent React and TypeScript proficiency",
        "Strong portfolio of production applications",
        "Good understanding of modern development workflows",
        "Experience with testing frameworks",
      ],
      concerns: ["Limited backend experience", "No experience with our specific tech stack (Next.js)"],
      recommendation: "Strong candidate - recommend for technical interview",
    },
  }

  return applicants[id as keyof typeof applicants] || null
}

interface ApplicantAnalysisProps {
  applicantId: string
}

export function ApplicantAnalysis({ applicantId }: ApplicantAnalysisProps) {
  const applicant = getApplicantData(applicantId)

  if (!applicant) {
    return (
      <div className="flex flex-1 flex-col">
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator orientation="vertical" className="mr-2 h-4" />
          <Link href="/">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>
          </Link>
        </header>
        <div className="flex flex-1 items-center justify-center">
          <p>Applicant not found</p>
        </div>
      </div>
    )
  }

  const getScoreColor = (score: number) => {
    if (score >= 85) return "text-green-600"
    if (score >= 70) return "text-yellow-600"
    return "text-red-600"
  }

  const getScoreBadgeVariant = (score: number) => {
    if (score >= 85) return "default"
    if (score >= 70) return "secondary"
    return "destructive"
  }

  return (
    <div className="flex flex-1 flex-col">
      <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mr-2 h-4" />
        <Link href="/">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
        </Link>
        <div className="ml-auto flex gap-2">
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Download Resume
          </Button>
          <Button size="sm">
            <Mail className="h-4 w-4 mr-2" />
            Contact
          </Button>
        </div>
      </header>

      <div className="flex-1 p-6 space-y-6">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold">{applicant.name}</h1>
            <p className="text-muted-foreground">{applicant.position}</p>
            <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
              <div className="flex items-center gap-1">
                <Mail className="h-4 w-4" />
                {applicant.email}
              </div>
              <div className="flex items-center gap-1">
                <Phone className="h-4 w-4" />
                {applicant.phone}
              </div>
            </div>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold mb-1">
              <Badge
                variant={getScoreBadgeVariant(applicant.overallScore)}
                className={`text-lg px-3 py-1 ${getScoreColor(applicant.overallScore)}`}
              >
                {applicant.overallScore}%
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground">Overall AI Fit Score</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Skills Analysis */}
          <Card>
            <CardHeader>
              <CardTitle>Skills Analysis</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {applicant.skills.map((skill) => (
                <div key={skill.name} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-2">
                      <span className="font-medium">{skill.name}</span>
                      {skill.required && (
                        <Badge variant="outline" className="text-xs">
                          Required
                        </Badge>
                      )}
                    </div>
                    <span className={`font-medium ${getScoreColor(skill.score)}`}>{skill.score}%</span>
                  </div>
                  <Progress value={skill.score} className="h-2" />
                </div>
              ))}
            </CardContent>
          </Card>

          {/* AI Summary */}
          <Card>
            <CardHeader>
              <CardTitle>AI Analysis Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-medium mb-2">Overview</h4>
                <p className="text-sm text-muted-foreground">{applicant.summary}</p>
              </div>

              <div>
                <h4 className="font-medium mb-2 text-green-600">Strengths</h4>
                <ul className="text-sm text-muted-foreground space-y-1">
                  {applicant.strengths.map((strength, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <span className="text-green-500 mt-1">•</span>
                      {strength}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h4 className="font-medium mb-2 text-yellow-600">Areas of Concern</h4>
                <ul className="text-sm text-muted-foreground space-y-1">
                  {applicant.concerns.map((concern, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <span className="text-yellow-500 mt-1">•</span>
                      {concern}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="pt-4 border-t">
                <h4 className="font-medium mb-2">Recommendation</h4>
                <p className="text-sm font-medium text-green-600">{applicant.recommendation}</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Additional Info */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Experience</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">{applicant.experience}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Education</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">{applicant.education}</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}