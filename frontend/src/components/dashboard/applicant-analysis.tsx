"use client"

import { useState, useRef, useEffect } from "react"
import {
  ArrowLeft,
  Download,
  Mail,
  Phone,
  User,
  Sparkles,
  UserCheck,
  FileText,
  Target,
  CheckCircle,
  XCircle,
  Scale,
  Award,
  MapPin,
  Calendar,
  Clock,
  BrainCircuit,
  Zap,
  Briefcase
} from "lucide-react"
import Link from "next/link"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"
import { Label } from "@/components/ui/label"
import { detailedCandidates, jobPosts } from "@/lib/script";

// Mock detailed applicant data
const getApplicantData = (id: string) => {
  return detailedCandidates.find(c => c.id === id) || null;
}

interface ApplicantAnalysisProps {
  applicantId: string
}

export function ApplicantAnalysis({ applicantId }: ApplicantAnalysisProps) {
  const [showTranscript, setShowTranscript] = useState(false)
  const transcriptRef = useRef<HTMLDivElement>(null)
  const applicant = getApplicantData(applicantId)
  const job = applicant
    ? jobPosts.find(j => j.id === (applicant as any).jobId)
    : null

  useEffect(() => {
    if (showTranscript && transcriptRef.current) {
      setTimeout(() => {
        transcriptRef.current?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }, 100)
    }
  }, [showTranscript])

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
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-violet-600">
            <User className="h-4 w-4 text-white" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 via-blue-800 to-violet-800 bg-clip-text text-transparent dark:from-white dark:via-blue-200 dark:to-violet-200">
            {applicant.name}
          </h1>
        </div>
        <Separator orientation="vertical" className="h-6" />
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gradient-to-r from-blue-50 to-violet-50 border border-blue-200/50 dark:from-blue-950/50 dark:to-violet-950/50 dark:border-blue-800/30">
            <Zap className="h-3.5 w-3.5 text-blue-600 dark:text-blue-400" />
            <span className={`text-sm font-bold ${getScoreColor(applicant.overallScore)}`}>
              {applicant.overallScore}
            </span>
          </div>
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
            className="gap-2 bg-slate-900 text-white hover:bg-slate-700 dark:bg-slate-50 dark:text-slate-900 dark:hover:bg-slate-200"
          >
            <Mail className="h-4 w-4" />
            Contact
          </Button>
        </div>
      </header>

      <div className="flex-1 p-8 space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-slate-800 via-blue-700 to-violet-700 bg-clip-text text-transparent dark:from-white dark:via-blue-300 dark:to-violet-300">
            Analysis for {applicant.name}
          </h1>
          {job && (
            <p className="mt-2 text-lg text-slate-600 dark:text-slate-400">
              Applied for:{" "}
              <span className="font-semibold text-slate-700 dark:text-slate-300">
                {job.title}
              </span>
            </p>
          )}
        </div>

        {/* Final Decision Card */}
        <Card className="bg-gradient-to-br from-slate-50 to-white dark:from-slate-900 dark:to-slate-800/70 border-t-4 border-b-0 border-x-0 border-violet-500 shadow-xl">
          <CardHeader>
            <CardTitle className="flex items-center justify-center gap-3 text-2xl">
              <Scale className="h-6 w-6 text-violet-500"/>
              The Verdict
            </CardTitle>
          </CardHeader>
          <CardContent className="text-center space-y-4">
            <div className="flex flex-col items-center justify-center gap-2">
                <div className={`inline-flex items-center justify-center rounded-full px-6 py-2 text-2xl font-bold ${applicant.decision === 'HIRE' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-300' : 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300'}`}>
                  {applicant.decision}
                </div>
                <p className="text-lg text-slate-600 dark:text-slate-400">
                  with <span className="font-bold text-slate-800 dark:text-slate-200">{(applicant.confidence * 100).toFixed(0)}%</span> confidence
                </p>
            </div>
            <div className="max-w-3xl mx-auto text-left pt-4">
              <p className="mt-1 text-slate-700 dark:text-slate-300 italic text-center">"{applicant.recommendation}"</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto text-left pt-4">
              <div className="space-y-2">
                <h3 className="font-semibold text-lg text-emerald-600 dark:text-emerald-400">Strengths</h3>
                <ul className="space-y-2">
                  {applicant.strengths.map((strength, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-600 dark:text-slate-400">
                       <CheckCircle className="h-4 w-4 mt-0.5 text-emerald-500 shrink-0"/>
                       <span>{strength}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="space-y-2">
                <h3 className="font-semibold text-lg text-red-600 dark:text-red-400">Concerns</h3>
                 <ul className="space-y-2">
                  {applicant.concerns.map((concern, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-600 dark:text-slate-400">
                       <XCircle className="h-4 w-4 mt-0.5 text-red-500 shrink-0"/>
                       <span>{concern}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="max-w-3xl mx-auto text-left pt-4">
              <Label className="font-semibold text-center block">Key Factors in Decision</Label>
              <div className="mt-2 flex flex-wrap gap-2 justify-center">
                {applicant.keyFactors.map((factor, index) => (
                  <Badge key={index} className="bg-amber-100 border-amber-300 text-amber-800 dark:bg-amber-900/50 dark:text-amber-300 dark:border-amber-700">{factor}</Badge>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Contact Information */}
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><User className="h-5 w-5 text-violet-500"/>Contact Information</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex items-center gap-3 p-4 rounded-lg bg-slate-50 dark:bg-slate-800/50">
                <Mail className="h-5 w-5 text-blue-500" />
                <div>
                  <Label className="text-sm font-medium text-slate-700 dark:text-slate-300">Email</Label>
                  <p className="text-slate-900 dark:text-white font-medium">{applicant.email}</p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-4 rounded-lg bg-slate-50 dark:bg-slate-800/50">
                <Phone className="h-5 w-5 text-green-500" />
                <div>
                  <Label className="text-sm font-medium text-slate-700 dark:text-slate-300">Phone</Label>
                  <p className="text-slate-900 dark:text-white font-medium">{applicant.phone}</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Main Analysis Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Resume Breakdown Card */}
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><FileText className="h-5 w-5 text-blue-500"/>Resume Breakdown</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center">
                <Label>Experience Level</Label>
                <Badge variant="secondary">{applicant.experienceLevel}</Badge>
              </div>
              <div className="flex justify-between items-center">
                <Label>Years of Experience</Label>
                <Badge variant="outline">{applicant.experienceYears} years</Badge>
              </div>
              <div>
                <Label className="mb-2 block">Technical Skills</Label>
                <div className="flex flex-wrap gap-2">
                  {applicant.skills.map((skill, index) => (
                    <Badge key={index} className={skill.required ? "bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300" : ""}>
                      {skill.name}
                    </Badge>
                  ))}
                </div>
              </div>
              <div>
                <Label className="mb-2 block">Key Achievements</Label>
                <ul className="space-y-2">
                  {applicant.achievements.map((achievement, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                      <CheckCircle className="h-4 w-4 mt-0.5 text-emerald-500 shrink-0"/>
                      <span>{achievement}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </CardContent>
          </Card>
          
          {/* Candidate-Job Fit Card */}
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><Target className="h-5 w-5 text-emerald-500"/>Candidate-Job Fit</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label className="mb-2 block">Skill Matches</Label>
                <div className="flex flex-wrap gap-2">
                  {applicant.skillMatches.map((skill, index) => (
                    <Badge key={index} className="bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-300">{skill}</Badge>
                  ))}
                </div>
              </div>
              <div>
                <Label className="mb-2 block">Skill Gaps</Label>
                <div className="flex flex-wrap gap-2">
                  {applicant.skillGaps.map((skill, index) => (
                    <Badge key={index} variant="destructive">{skill}</Badge>
                  ))}
                </div>
              </div>
              <div className="flex justify-between items-center">
                <Label>Experience Match</Label>
                <Badge variant="outline">{applicant.experienceMatch}</Badge>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Debate Transcript Section */}
        <div className="text-center">
          <Button variant="secondary" onClick={() => setShowTranscript(!showTranscript)}>
            {showTranscript ? "Hide" : "Show"} Full Evaluation Transcript
          </Button>
        </div>

        {showTranscript && (
          <Card className="shadow-lg" ref={transcriptRef}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BrainCircuit className="h-5 w-5 text-purple-500" />
                Full Evaluation Transcript
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {applicant.transcript.map((turn, index) => {
                if (turn.position === 'evaluation') {
                  return (
                    <div key={index} className="p-4 rounded-lg bg-blue-50 dark:bg-blue-900/30">
                      <h4 className="font-semibold text-lg mb-2 flex items-center gap-2 text-blue-600 dark:text-blue-400">
                        <Target className="h-5 w-5" />
                        {turn.agent_name}'s Assessment
                      </h4>
                      <p className="text-slate-700 dark:text-slate-300">{turn.content}</p>
                    </div>
                  )
                }
                if (turn.position === 'pro' || turn.position === 'anti') {
                  const isPro = turn.position === 'pro';
                  return (
                    <div key={index} className={`p-4 rounded-lg ${isPro ? 'bg-emerald-50 dark:bg-emerald-900/30' : 'bg-red-50 dark:bg-red-900/30'}`}>
                      <h4 className={`font-semibold text-lg mb-2 flex items-center gap-2 ${isPro ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'}`}>
                        {isPro ? <CheckCircle className="h-5 w-5" /> : <XCircle className="h-5 w-5" />}
                         {turn.agent_name}'s Argument (Round {Math.floor(index / 2) + (index % 2)})
                      </h4>
                      <p className="text-slate-700 dark:text-slate-300">{turn.content}</p>
                    </div>
                  )
                }
                return null;
              })}
              
              {/* Final Decision in Transcript */}
              <div className="!mt-8 pt-6 border-t-2 border-dashed border-violet-300 dark:border-violet-700">
                 <div className="p-4 rounded-lg bg-violet-50 dark:bg-violet-900/40 ring-1 ring-violet-200 dark:ring-violet-800">
                  <h4 className="font-semibold text-lg mb-2 flex items-center gap-2 text-violet-600 dark:text-violet-400">
                    <Scale className="h-5 w-5" />
                    Decision Agent's Final Assessment
                  </h4>
                  <p className="text-slate-700 dark:text-slate-300 italic mb-4">
                    "{applicant.recommendation}"
                  </p>
                   <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      <div className="space-y-1">
                          <h5 className="font-semibold text-emerald-600 dark:text-emerald-500">Pros</h5>
                          <ul className="list-disc list-inside text-slate-600 dark:text-slate-400">
                              {applicant.strengths.map((strength, i) => <li key={`pro-${i}`}>{strength}</li>)}
                          </ul>
                      </div>
                      <div className="space-y-1">
                          <h5 className="font-semibold text-red-600 dark:text-red-500">Cons</h5>
                          <ul className="list-disc list-inside text-slate-600 dark:text-slate-400">
                              {applicant.concerns.map((concern, i) => <li key={`con-${i}`}>{concern}</li>)}
                          </ul>
                      </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}