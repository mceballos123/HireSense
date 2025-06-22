"use client"

import { useState } from "react"
import { ChevronDown, ChevronUp, Filter } from "lucide-react"
import Link from "next/link"
import React from "react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Separator } from "@/components/ui/separator"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { SidebarTrigger } from "@/components/ui/sidebar"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { jobPosts } from "@/lib/script"

type SortOption = "score-high" | "score-low" | "name"
type JobPost = (typeof jobPosts)[number]

const applicants = [
  {
    id: 1,
    name: "Sarah Johnson",
    position: "Senior Frontend Developer",
    score: 92,
    summary:
      "Excellent React and TypeScript skills. 5+ years experience with modern frameworks. Strong portfolio of responsive web applications.",
  },
  {
    id: 2,
    name: "Michael Chen",
    position: "Backend Engineer",
    score: 88,
    summary:
      "Solid Node.js and Python experience. Good understanding of microservices architecture. Previous experience at scale-up companies.",
  },
  {
    id: 3,
    name: "Emily Rodriguez",
    position: "Full Stack Developer",
    score: 76,
    summary:
      "Well-rounded skills in both frontend and backend. Some gaps in advanced database optimization but shows strong learning potential.",
  },
  {
    id: 4,
    name: "David Kim",
    position: "Senior Frontend Developer",
    score: 84,
    summary:
      "Strong Vue.js background, transitioning to React. Good design sense and UX awareness. Solid technical foundation.",
  },
  {
    id: 5,
    name: "Lisa Thompson",
    position: "Backend Engineer",
    score: 71,
    summary:
      "Junior-level experience but shows promise. Good grasp of fundamentals. Would benefit from mentorship in system design.",
  },
]

export function DashboardContent() {
  const [sortBy, setSortBy] = useState<SortOption>("score-high")
  const [expandedRows, setExpandedRows] = useState<Set<number>>(new Set())
  const [selectedJob, setSelectedJob] = useState<JobPost | null>(null)

  const sortedApplicants = [...applicants].sort((a, b) => {
    switch (sortBy) {
      case "score-high":
        return b.score - a.score
      case "score-low":
        return a.score - b.score
      case "name":
        return a.name.localeCompare(b.name)
      default:
        return 0
    }
  })

  const toggleRow = (id: number) => {
    setExpandedRows((prev) => {
      const updated = new Set(prev)
      updated.has(id) ? updated.delete(id) : updated.add(id)
      return updated
    })
  }

  const getScoreBadgeClass = (score: number) =>
    score >= 85
      ? "bg-green-600 text-white"
      : score >= 70
      ? "bg-yellow-500 text-white"
      : "bg-red-600 text-white"

  return (
    <div className="flex flex-1 flex-col">
      <header className="flex h-16 items-center gap-2 border-b px-4">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mr-2 h-4" />
        <h1 className="text-lg font-semibold">Dashboard</h1>
      </header>

      <div className="flex flex-1 gap-4 p-4">
        {/* Applicants Table */}
        <div className="flex-1 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">Applicants</h2>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" size="sm">
                  <Filter className="h-4 w-4 mr-2" />
                  Sort by
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={() => setSortBy("score-high")}>
                  Score (High to Low)
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setSortBy("score-low")}>
                  Score (Low to High)
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setSortBy("name")}>
                  Name (A-Z)
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>

          <Card>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Position</TableHead>
                  <TableHead>AI Fit Score</TableHead>
                  <TableHead className="w-[50px]" />
                </TableRow>
              </TableHeader>
              <TableBody>
                {sortedApplicants.map((applicant) => (
                  <React.Fragment key={applicant.id}>
                    <TableRow className="cursor-pointer">
                      <TableCell>
                        <Link
                          href={`/applicant/${applicant.id}`}
                          className="font-medium text-blue-600 hover:text-blue-800 hover:underline"
                        >
                          {applicant.name}
                        </Link>
                      </TableCell>
                      <TableCell>{applicant.position}</TableCell>
                      <TableCell>
                        <Badge className={getScoreBadgeClass(applicant.score)}>
                          {applicant.score}%
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => toggleRow(applicant.id)}
                        >
                          {expandedRows.has(applicant.id) ? (
                            <ChevronUp className="h-4 w-4" />
                          ) : (
                            <ChevronDown className="h-4 w-4" />
                          )}
                        </Button>
                      </TableCell>
                    </TableRow>
                    {expandedRows.has(applicant.id) && (
                      <TableRow>
                        <TableCell colSpan={4} className="bg-muted/50">
                          <div className="py-2">
                            <p className="text-sm text-muted-foreground">
                              <strong>AI Summary:</strong> {applicant.summary}
                            </p>
                          </div>
                        </TableCell>
                      </TableRow>
                    )}
                  </React.Fragment>
                ))}
              </TableBody>
            </Table>
          </Card>
        </div>

        {/* Job Posts Sidebar */}
        <div className="w-80 space-y-4">
          <h2 className="text-xl font-semibold">Active Job Posts</h2>
          <div className="space-y-3">
            {jobPosts.map((job) => (
              <Dialog key={job.id}>
                <DialogTrigger asChild>
                  <Card
                    onClick={() => setSelectedJob(job)}
                    className="cursor-pointer transition hover:shadow-md"
                  >
                    <CardHeader className="pb-2">
                      <CardTitle className="text-sm">{job.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-xs text-muted-foreground mb-2">{job.summary}</p>
                      <div className="flex justify-between items-center">
                        <span className="text-xs text-muted-foreground">
                          {job.applicants} applicants
                        </span>
                        <Button variant="outline" size="sm">
                          View
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>{selectedJob?.title}</DialogTitle>
                  </DialogHeader>
                  <div className="mt-2 space-y-6 text-sm">
                    <p className="text-white">
                      <strong>Description:</strong> {selectedJob?.description}
                    </p>

                    <div>
                      <p className="font-medium text-foreground">Responsibilities</p>
                      <ul className="list-disc list-inside space-y-1 text-muted-foreground">
                        {selectedJob?.responsibilities.map((item) => (
                          <li key={item}>{item}</li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <p className="font-medium text-foreground">Qualifications</p>
                      <ul className="list-disc list-inside space-y-1 text-muted-foreground">
                        {selectedJob?.qualifications.map((item) => (
                          <li key={item}>{item}</li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <p className="font-medium text-foreground">Bonus</p>
                      <ul className="list-disc list-inside space-y-1 text-muted-foreground">
                        {selectedJob?.bonus.map((item) => (
                          <li key={item}>{item}</li>
                        ))}
                      </ul>
                    </div>

                    {selectedJob?.technologies && (
                      <div>
                        <p className="font-medium text-foreground">Technologies</p>
                        <div className="flex flex-wrap gap-2 mt-2">
                          {selectedJob.technologies.map((tech) => (
                            <span
                              key={tech}
                              className="px-3 py-1 text-xs font-medium rounded-full bg-purple-900 text-purple-300 border border-purple-700"
                            >
                              {tech}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </DialogContent>
              </Dialog>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}





