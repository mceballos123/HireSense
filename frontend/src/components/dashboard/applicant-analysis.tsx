"use client"

import {
  ArrowLeft,
  Download,
  Mail,
  Phone,
  User,
  Sparkles,
  UserCheck,
} from "lucide-react"
import Link from "next/link"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"
import { Label } from "@/components/ui/label"

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
      <div className="flex flex-1 flex-col bg-gradient-to-br from-slate-50 via-white to-blue-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-blue-950/20">
        <header className="flex h-20 items-center gap-3 border-b border-white/20 bg-white/70 backdrop-blur-xl px-8 shadow-sm dark:bg-slate-900/70 dark:border-slate-800/50">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-violet-600">
              <UserCheck className="h-4 w-4 text-white" />
            </div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-slate-900 via-blue-800 to-violet-800 bg-clip-text text-transparent dark:from-white dark:via-blue-200 dark:to-violet-200">
              Applicant Analysis
            </h1>
          </div>
        </header>
        <div className="flex flex-col items-center justify-center h-full text-center text-slate-500 dark:text-slate-400 p-8">
          <User className="h-12 w-12 mx-auto mb-4 text-slate-400" />
          <h3 className="text-xl font-semibold mb-2 text-slate-700 dark:text-slate-300">
            Select an Applicant
          </h3>
          <p>
            Choose an applicant from the list to view their detailed analysis.
          </p>
        </div>
      </div>
    )
  }

  const getScoreColor = (score: number) => {
    if (score >= 85) return "text-emerald-600 dark:text-emerald-400"
    if (score >= 70) return "text-amber-600 dark:text-amber-400"
    return "text-red-600 dark:text-red-400"
  }

  const getScoreBadgeVariant = (score: number) => {
    if (score >= 85) return "bg-emerald-500 text-white border-0"
    if (score >= 70) return "bg-amber-500 text-white border-0"
    return "bg-red-500 text-white border-0"
  }

  return (
    <div className="flex flex-1 flex-col bg-gradient-to-br from-slate-50 via-white to-blue-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-blue-950/20">
      <header className="flex h-20 items-center gap-3 border-b border-white/20 bg-white/70 backdrop-blur-xl px-8 shadow-sm dark:bg-slate-900/70 dark:border-slate-800/50">
        <Link href="/">
          <Button
            variant="ghost"
            size="sm"
            className="gap-2 hover:bg-slate-100 dark:hover:bg-slate-800"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </Button>
        </Link>
        <Separator orientation="vertical" className="h-6" />
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-violet-600">
            <Sparkles className="h-4 w-4 text-white" />
          </div>
          <h1 className="text-xl font-bold bg-gradient-to-r from-slate-900 via-blue-800 to-violet-800 bg-clip-text text-transparent dark:from-white dark:via-blue-200 dark:to-violet-200">
            Applicant Analysis
          </h1>
        </div>
        <div className="ml-auto flex gap-3">
          <Button
            variant="outline"
            size="sm"
            className="gap-2 border-slate-300 hover:bg-slate-50 dark:border-slate-600 dark:hover:bg-slate-800"
          >
            <Download className="h-4 w-4" />
            Download Resume
          </Button>
          <Button
            size="sm"
            className="gap-2 bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 text-white border-0 shadow-lg shadow-blue-500/25"
          >
            <Mail className="h-4 w-4" />
            Contact
          </Button>
        </div>
      </header>

      <div className="flex-1 p-8 space-y-8">
        {/* Header */}
        <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm dark:bg-slate-800/90 dark:border-slate-700/60">
          <CardContent className="p-8">
            <div className="flex items-start justify-between">
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="p-3 rounded-lg bg-gradient-to-br from-blue-600 to-violet-600">
                    <User className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white">{applicant.name}</h1>
                    <p className="text-lg text-slate-600 dark:text-slate-400 font-medium">{applicant.position}</p>
                  </div>
                </div>
                <div className="flex items-center gap-6 text-sm text-slate-600 dark:text-slate-400">
                  <div className="flex items-center gap-2">
                    <Mail className="h-4 w-4" />
                    <span>{applicant.email}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Phone className="h-4 w-4" />
                    <span>{applicant.phone}</span>
                  </div>
                </div>
              </div>
              <div className="text-center space-y-2">
                <div className="flex items-center justify-center gap-2 p-4 rounded-xl bg-gradient-to-br from-emerald-50 to-teal-50 border border-emerald-200/50 dark:from-emerald-950/50 dark:to-teal-950/50 dark:border-emerald-800/30">
                  <Sparkles className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
                  <div className="text-3xl font-bold text-emerald-600 dark:text-emerald-400">
                    {applicant.overallScore}%
                  </div>
                </div>
                <p className="text-sm font-medium text-slate-600 dark:text-slate-400">Overall AI Fit Score</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Skills Analysis */}
          <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm hover:shadow-md transition-shadow dark:bg-slate-800/90 dark:border-slate-700/60">
            <CardHeader className="pb-6">
              <CardTitle className="text-xl font-bold text-slate-900 dark:text-white">Skills Analysis</CardTitle>
              <p className="text-slate-600 dark:text-slate-400">AI-evaluated technical competencies</p>
            </CardHeader>
            <CardContent className="space-y-6">
              {applicant.skills.map((skill) => (
                <div key={skill.name} className="space-y-3">
                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-3">
                      <span className="font-medium text-slate-900 dark:text-white">{skill.name}</span>
                      {skill.required && (
                        <Badge variant="outline" className="text-xs border-blue-200 text-blue-700 bg-blue-50 dark:border-blue-800/30 dark:text-blue-400 dark:bg-blue-950/50">
                          Required
                        </Badge>
                      )}
                    </div>
                    <span className={`font-bold text-lg ${getScoreColor(skill.score)}`}>{skill.score}%</span>
                  </div>
                  <Progress value={skill.score} className="h-3" />
                </div>
              ))}
            </CardContent>
          </Card>

          {/* AI Summary */}
          <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm hover:shadow-md transition-shadow dark:bg-slate-800/90 dark:border-slate-700/60">
            <CardHeader className="pb-6">
              <CardTitle className="text-xl font-bold text-slate-900 dark:text-white">AI Analysis Summary</CardTitle>
              <p className="text-slate-600 dark:text-slate-400">Comprehensive candidate evaluation</p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="p-4 rounded-lg bg-slate-50 border border-slate-200/50 dark:bg-slate-800/50 dark:border-slate-700/50">
                <h4 className="font-bold text-base mb-3 text-slate-900 dark:text-white">Overview</h4>
                <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300">{applicant.summary}</p>
              </div>

              <div className="p-4 rounded-lg bg-emerald-50 border border-emerald-200/50 dark:bg-emerald-900/20 dark:border-emerald-800/30">
                <h4 className="font-bold text-base mb-3 flex items-center gap-2 text-emerald-800 dark:text-emerald-200">
                  ✓ Key Strengths
                </h4>
                <ul className="space-y-2">
                  {applicant.strengths.map((strength, index) => (
                    <li key={index} className="text-sm flex items-start gap-2 text-emerald-700 dark:text-emerald-300">
                      <span className="text-emerald-500 mt-1 text-xs">●</span>
                      {strength}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="p-4 rounded-lg bg-amber-50 border border-amber-200/50 dark:bg-amber-900/20 dark:border-amber-800/30">
                <h4 className="font-bold text-base mb-3 flex items-center gap-2 text-amber-800 dark:text-amber-200">
                  ⚠ Areas of Concern
                </h4>
                <ul className="space-y-2">
                  {applicant.concerns.map((concern, index) => (
                    <li key={index} className="text-sm flex items-start gap-2 text-amber-700 dark:text-amber-300">
                      <span className="text-amber-500 mt-1 text-xs">●</span>
                      {concern}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="p-4 rounded-lg bg-blue-50 border border-blue-200/50 dark:bg-blue-900/20 dark:border-blue-800/30">
                <h4 className="font-bold text-base mb-3 flex items-center gap-2 text-blue-800 dark:text-blue-200">
                  💡 Recommendation
                </h4>
                <p className="text-sm text-blue-700 dark:text-blue-300 font-medium">{applicant.recommendation}</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Additional Details */}
        <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm dark:bg-slate-800/90 dark:border-slate-700/60">
          <CardHeader>
            <CardTitle className="text-xl font-bold text-slate-900 dark:text-white">Additional Information</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label className="text-sm font-medium text-slate-700 dark:text-slate-300">Experience</Label>
                <p className="text-slate-900 dark:text-white font-medium">{applicant.experience}</p>
              </div>
              <div className="space-y-2">
                <Label className="text-sm font-medium text-slate-700 dark:text-slate-300">Education</Label>
                <p className="text-slate-900 dark:text-white font-medium">{applicant.education}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}