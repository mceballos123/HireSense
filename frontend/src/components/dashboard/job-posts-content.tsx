"use client"

import { useState } from "react"
import { Plus, Users, Calendar, MapPin, Briefcase } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { jobPosts } from "@/lib/script"
import { CreateJobForm } from "./create-job-form"
import Link from "next/link"

export function JobPostsContent() {
  const [createJobOpen, setCreateJobOpen] = useState(false)

  return (
    <div className="flex flex-1 flex-col bg-gradient-to-br from-slate-50 via-white to-blue-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-blue-950/20">
      <header className="flex h-20 items-center gap-3 border-b border-white/20 bg-white/70 backdrop-blur-xl px-8 shadow-sm dark:bg-slate-900/70 dark:border-slate-800/50">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-violet-600">
            <Briefcase className="h-4 w-4 text-white" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 via-blue-800 to-violet-800 bg-clip-text text-transparent dark:from-white dark:via-blue-200 dark:to-violet-200">
            Job Posts
          </h1>
        </div>
        <div className="ml-auto">
          <Button 
            onClick={() => setCreateJobOpen(true)}
            className="gap-2 bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 text-white border-0 shadow-lg shadow-blue-500/25"
          >
            <Plus className="h-4 w-4" />
            New Job Post
          </Button>
        </div>
      </header>

      <div className="flex-1 p-8">
        <div className="grid gap-6">
          {jobPosts.map((job) => (
            <Card key={job.id} className="group relative overflow-hidden border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm hover:shadow-xl hover:border-blue-300/60 transition-all duration-300 hover:-translate-y-1 dark:bg-slate-800/90 dark:border-slate-700/60 dark:hover:border-blue-600/60">
              <CardHeader className="pb-4">
                <div className="flex items-start justify-between">
                  <div className="space-y-2">
                    <CardTitle className="text-xl font-bold text-slate-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                      {job.title}
                    </CardTitle>
                    <div className="flex items-center gap-4 text-sm text-slate-500 dark:text-slate-400">
                      <div className="flex items-center gap-1">
                        <Calendar className="h-4 w-4" />
                        <span>Posted {job.posted}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Users className="h-4 w-4" />
                        <span className="font-semibold text-slate-700 dark:text-slate-300">{job.applicants}</span>
                        <span>applicants</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge className="bg-gradient-to-r from-emerald-500 to-teal-500 text-white border-0 shadow-lg shadow-emerald-500/20">
                      {job.status}
                    </Badge>
                  </div>
                </div>
              </CardHeader>

              <CardContent className="space-y-4">
                <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                  {job.summary}
                </p>
                
                {job.technologies && (
                  <div className="flex flex-wrap gap-2">
                    {job.technologies.slice(0, 4).map((tech) => (
                      <Badge
                        key={tech}
                        className="bg-slate-100 text-slate-700 border border-slate-200 hover:bg-slate-200 transition-colors dark:bg-slate-700 dark:text-slate-300 dark:border-slate-600"
                      >
                        {tech}
                      </Badge>
                    ))}
                    {job.technologies.length > 4 && (
                      <Badge variant="outline" className="border-slate-300 text-slate-600 dark:border-slate-600 dark:text-slate-400">
                        +{job.technologies.length - 4} more
                      </Badge>
                    )}
                  </div>
                )}
                
                <div className="flex items-center justify-between pt-4 border-t border-slate-200/50 dark:border-slate-700/50">
                  <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
                    <MapPin className="h-4 w-4" />
                    <span>Remote • Full-time</span>
                  </div>
                  <Link href={`/job-posts/${job.id}`}>
                    <Button size="sm" className="bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 text-white border-0 shadow-sm opacity-0 group-hover:opacity-100 transition-all duration-300">
                      View Details
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      <CreateJobForm open={createJobOpen} onOpenChange={setCreateJobOpen} />
    </div>
  )
}




