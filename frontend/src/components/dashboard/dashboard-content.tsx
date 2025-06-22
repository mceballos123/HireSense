"use client"

import { useState } from "react"
import Link from "next/link"
import React from "react"
import { 
  Users, 
  Briefcase, 
  TrendingUp, 
  Clock,
  Star,
  MapPin,
  Calendar,
  ChevronDown,
  ChevronRight,
  Sparkles,
  Target,
  Zap
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { SidebarTrigger } from "@/components/ui/sidebar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { jobPosts } from "@/lib/script"

type JobPost = (typeof jobPosts)[number]
type SortOption = "score-high" | "score-low" | "name" | "date-recent" | "date-old"

const applicants = [
  {
    id: 1,
    name: "Sarah Johnson",
    position: "Senior Frontend Developer",
    location: "San Francisco, CA",
    experience: "5+ years",
    skills: ["React", "TypeScript", "Next.js"],
    status: "Under Review",
    appliedDate: "2024-01-15",
    score: 95
  },
  {
    id: 2,
    name: "Michael Chen",
    position: "Backend Engineer",
    location: "Seattle, WA",
    experience: "4 years",
    skills: ["Node.js", "Python", "AWS"],
    status: "Interview Scheduled",
    appliedDate: "2024-01-14",
    score: 88
  },
  {
    id: 3,
    name: "Emily Rodriguez",
    position: "Full Stack Developer",
    location: "Austin, TX",
    experience: "3 years",
    skills: ["React", "Node.js", "MongoDB"],
    status: "New",
    appliedDate: "2024-01-16",
    score: 82
  },
  {
    id: 4,
    name: "David Kim",
    position: "Senior Frontend Developer",
    location: "New York, NY",
    experience: "6 years",
    skills: ["Vue.js", "React", "GraphQL"],
    status: "Under Review",
    appliedDate: "2024-01-13",
    score: 91
  },
  {
    id: 5,
    name: "Lisa Thompson",
    position: "Backend Engineer",
    location: "Denver, CO",
    experience: "2 years",
    skills: ["Python", "Django", "PostgreSQL"],
    status: "New",
    appliedDate: "2024-01-17",
    score: 76
  },
]

const dashboardStats = [
  {
    title: "Total Applicants",
    value: "2,847",
    change: "+23%",
    trend: "up",
    icon: Users,
    description: "vs last month",
    gradient: "from-blue-600 via-blue-500 to-cyan-400"
  },
  {
    title: "Open Positions",
    value: "12",
    change: "+4",
    trend: "up",
    icon: Briefcase,
    description: "active roles",
    gradient: "from-emerald-600 via-emerald-500 to-teal-400"
  },
  {
    title: "Interview Rate",
    value: "68%",
    change: "+12%",
    trend: "up",
    icon: Target,
    description: "conversion",
    gradient: "from-violet-600 via-purple-500 to-fuchsia-400"
  },
  {
    title: "Avg. Time to Hire",
    value: "14d",
    change: "-3d",
    trend: "up",
    icon: Clock,
    description: "faster hiring",
    gradient: "from-orange-600 via-amber-500 to-yellow-400"
  }
]

const getStatusColor = (status: string) => {
  switch (status) {
    case "New":
      return "bg-emerald-500/10 text-emerald-700 border border-emerald-200 dark:bg-emerald-400/10 dark:text-emerald-400 dark:border-emerald-800/30"
    case "Under Review":
      return "bg-blue-500/10 text-blue-700 border border-blue-200 dark:bg-blue-400/10 dark:text-blue-400 dark:border-blue-800/30"
    case "Interview Scheduled":
      return "bg-violet-500/10 text-violet-700 border border-violet-200 dark:bg-violet-400/10 dark:text-violet-400 dark:border-violet-800/30"
    default:
      return "bg-slate-100 text-slate-700 border border-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700"
  }
}

const getScoreColor = (score: number) => {
  if (score >= 90) return "text-emerald-600 dark:text-emerald-400"
  if (score >= 80) return "text-blue-600 dark:text-blue-400"
  if (score >= 70) return "text-amber-600 dark:text-amber-400"
  return "text-slate-600 dark:text-slate-400"
}

const getSortLabel = (sortBy: SortOption) => {
  switch (sortBy) {
    case "score-high":
      return "Score (High to Low)"
    case "score-low":
      return "Score (Low to High)"
    case "name":
      return "Name (A-Z)"
    case "date-recent":
      return "Date (Most Recent)"
    case "date-old":
      return "Date (Oldest First)"
    default:
      return "Sort by"
  }
}

export function DashboardContent() {
  const [selectedJob, setSelectedJob] = useState<JobPost | null>(null)
  const [sortBy, setSortBy] = useState<SortOption>("score-high")

  const sortedApplicants = [...applicants].sort((a, b) => {
    switch (sortBy) {
      case "score-high":
        return b.score - a.score
      case "score-low":
        return a.score - b.score
      case "name":
        return a.name.localeCompare(b.name)
      case "date-recent":
        return new Date(b.appliedDate).getTime() - new Date(a.appliedDate).getTime()
      case "date-old":
        return new Date(a.appliedDate).getTime() - new Date(b.appliedDate).getTime()
      default:
        return 0
    }
  })

  return (
    <div className="flex flex-1 flex-col bg-gradient-to-br from-slate-50 via-white to-blue-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-blue-950/20">
      {/* Header */}
      <header className="flex h-20 items-center gap-3 border-b border-white/20 bg-white/70 backdrop-blur-xl px-8 shadow-sm dark:bg-slate-900/70 dark:border-slate-800/50">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mr-3 h-6" />
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-violet-600">
            <Sparkles className="h-4 w-4 text-white" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 via-blue-800 to-violet-800 bg-clip-text text-transparent dark:from-white dark:via-blue-200 dark:to-violet-200">
            Talent Intelligence
          </h1>
        </div>
        <div className="ml-auto flex items-center gap-3">
          <Badge className="bg-gradient-to-r from-emerald-500 to-teal-500 text-white border-0 shadow-lg shadow-emerald-500/20">
            <div className="mr-1 h-2 w-2 rounded-full bg-white animate-pulse" />
            Live Data
          </Badge>
        </div>
      </header>

      <div className="flex-1 p-8 space-y-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Applicants */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-3xl font-bold text-slate-900 dark:text-white">Top Candidates</h2>
                <p className="text-slate-600 dark:text-slate-400">AI-ranked applicants based on fit score</p>
              </div>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button className="gap-2 bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 text-white border-0 shadow-lg shadow-blue-500/25">
                    {getSortLabel(sortBy)}
                    <ChevronDown className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-48">
                  <DropdownMenuItem onClick={() => setSortBy("score-high")}>
                    Score (High to Low)
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => setSortBy("score-low")}>
                    Score (Low to High)
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => setSortBy("name")}>
                    Name (A-Z)
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => setSortBy("date-recent")}>
                    Date (Most Recent)
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => setSortBy("date-old")}>
                    Date (Oldest First)
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>

            <div className="space-y-4">
              {sortedApplicants.map((applicant, index) => (
                <Card key={applicant.id} className="group relative overflow-hidden border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm hover:shadow-lg hover:border-blue-300/60 transition-all duration-300 hover:-translate-y-0.5 dark:bg-slate-800/90 dark:border-slate-700/60 dark:hover:border-blue-600/60">
                  {/* AI Score indicator */}
                  <div className="absolute top-4 right-4">
                    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gradient-to-r from-blue-50 to-violet-50 border border-blue-200/50 dark:from-blue-950/50 dark:to-violet-950/50 dark:border-blue-800/30">
                      <Zap className="h-3.5 w-3.5 text-blue-600 dark:text-blue-400" />
                      <span className={`text-sm font-bold ${getScoreColor(applicant.score)}`}>
                        {applicant.score}
                      </span>
                    </div>
                  </div>
                  
                  <CardContent className="p-6 pr-20">
                    <div className="space-y-4">
                      {/* Header */}
                      <div className="space-y-2">
                        <h3 className="text-xl font-bold text-slate-900 dark:text-white">
                          {applicant.name}
                        </h3>
                        <p className="text-lg text-slate-600 dark:text-slate-400 font-medium">{applicant.position}</p>
                      </div>
                      
                      {/* Details */}
                      <div className="flex items-center gap-6 text-sm text-slate-500 dark:text-slate-400">
                        <div className="flex items-center gap-2">
                          <MapPin className="h-4 w-4" />
                          <span>{applicant.location}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Clock className="h-4 w-4" />
                          <span>{applicant.experience}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Calendar className="h-4 w-4" />
                          <span>{new Date(applicant.appliedDate).toLocaleDateString()}</span>
                        </div>
                      </div>

                      {/* Skills */}
                      <div className="flex items-center gap-2 flex-wrap">
                        {applicant.skills.slice(0, 4).map((skill) => (
                          <Badge key={skill} className="bg-slate-100 text-slate-700 border border-slate-200 hover:bg-slate-200 transition-colors dark:bg-slate-700 dark:text-slate-300 dark:border-slate-600">
                            {skill}
                          </Badge>
                        ))}
                        {applicant.skills.length > 4 && (
                          <Badge variant="outline" className="border-slate-300 text-slate-600 dark:border-slate-600 dark:text-slate-400">
                            +{applicant.skills.length - 4} more
                          </Badge>
                        )}
                      </div>

                      {/* Action button */}
                      <div className="pt-2">
                        <Link href={`/applicant/${applicant.id}`}>
                          <Button variant="ghost" size="sm" className="opacity-0 group-hover:opacity-100 transition-all duration-300 hover:bg-blue-50 hover:text-blue-600 dark:hover:bg-blue-900/20 dark:hover:text-blue-400 gap-2">
                            <span>View Profile</span>
                            <ChevronRight className="h-4 w-4" />
                          </Button>
                        </Link>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Active Job Posts */}
          <div className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold text-slate-900 dark:text-white">Open Roles</h2>
              <p className="text-slate-600 dark:text-slate-400">Currently accepting applications</p>
            </div>

            <div className="space-y-4">
              {jobPosts.slice(0, 4).map((job) => (
                <Dialog key={job.id}>
                  <DialogTrigger asChild>
                    <Card
                      className="group cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-1 border-0 bg-gradient-to-br from-white via-slate-50/50 to-blue-50/30 backdrop-blur-sm dark:from-slate-800 dark:via-slate-700/50 dark:to-blue-900/10"
                    >
                      <CardContent className="p-6 space-y-4">
                        <div className="flex items-start justify-between">
                          <h3 className="font-bold text-lg text-slate-900 group-hover:text-blue-600 transition-colors dark:text-white dark:group-hover:text-blue-400">
                            {job.title}
                          </h3>
                          <Badge className="bg-gradient-to-r from-emerald-500 to-teal-500 text-white border-0 shadow-lg shadow-emerald-500/20">
                            Active
                          </Badge>
                        </div>
                        
                        <p className="text-sm text-slate-600 line-clamp-2 dark:text-slate-400">
                          {job.summary}
                        </p>
                        
                        <div className="flex items-center justify-between pt-2">
                          <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
                            <Users className="h-4 w-4" />
                            <span className="font-semibold text-slate-700 dark:text-slate-300">{job.applicants}</span>
                            <span>applicants</span>
                          </div>
                          
                          <div className="flex items-center gap-1 text-blue-600 group-hover:text-blue-700 transition-colors dark:text-blue-400 dark:group-hover:text-blue-300">
                            <span className="text-sm font-semibold">View Details</span>
                            <ChevronRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </DialogTrigger>
                  
                  <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto bg-white dark:bg-slate-900">
                    <DialogHeader>
                      <DialogTitle className="text-2xl font-bold text-slate-900 dark:text-white">{job.title}</DialogTitle>
                    </DialogHeader>
                    <div className="mt-4 space-y-6">
                      <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 dark:bg-slate-800 dark:border-slate-700">
                        <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300">
                          <strong className="text-slate-900 dark:text-white">Description:</strong> {job.description}
                        </p>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-amber-50 p-4 rounded-lg border border-amber-200 dark:bg-amber-900/20 dark:border-amber-800/30">
                          <h4 className="font-bold text-base mb-3 flex items-center gap-2 text-amber-800 dark:text-amber-200">
                            <Star className="h-4 w-4 text-amber-600 dark:text-amber-400" />
                            Key Responsibilities
                          </h4>
                          <ul className="space-y-2">
                            {job.responsibilities.map((item, index) => (
                              <li key={index} className="text-sm flex items-start gap-2 text-amber-700 dark:text-amber-300">
                                <div className="h-1.5 w-1.5 rounded-full bg-amber-500 mt-2 flex-shrink-0" />
                                {item}
                              </li>
                            ))}
                          </ul>
                        </div>

                        <div className="bg-emerald-50 p-4 rounded-lg border border-emerald-200 dark:bg-emerald-900/20 dark:border-emerald-800/30">
                          <h4 className="font-bold text-base mb-3 flex items-center gap-2 text-emerald-800 dark:text-emerald-200">
                            <Briefcase className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
                            Requirements
                          </h4>
                          <ul className="space-y-2">
                            {job.qualifications.map((item, index) => (
                              <li key={index} className="text-sm flex items-start gap-2 text-emerald-700 dark:text-emerald-300">
                                <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 mt-2 flex-shrink-0" />
                                {item}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>

                      {job.technologies && (
                        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200 dark:bg-blue-900/20 dark:border-blue-800/30">
                          <h4 className="font-bold text-base mb-3 text-blue-800 dark:text-blue-200">Tech Stack</h4>
                          <div className="flex flex-wrap gap-2">
                            {job.technologies.map((tech) => (
                              <Badge
                                key={tech}
                                className="bg-blue-600 hover:bg-blue-700 text-white border-0 shadow-sm px-3 py-1 text-xs font-semibold"
                              >
                                {tech}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      )}

                      <div className="flex items-center justify-between pt-4 border-t border-slate-200 dark:border-slate-700">
                        <div className="flex items-center gap-4 text-sm text-slate-600 dark:text-slate-400">
                          <div className="flex items-center gap-2">
                            <Users className="h-4 w-4" />
                            <span className="font-semibold text-slate-700 dark:text-slate-300">{job.applicants} applicants</span>
                          </div>
                        </div>
                        <Button className="bg-blue-600 hover:bg-blue-700 text-white border-0 shadow-lg px-6 py-2 text-sm font-semibold">
                          View All Applicants
                        </Button>
                      </div>
                    </div>
                  </DialogContent>
                </Dialog>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}





