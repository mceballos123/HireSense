"use client"

import { Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { Badge } from "@/components/ui/badge"
import { jobPosts } from "@/lib/script"
import Link from "next/link"

export function JobPostsContent() {
  return (
    <div className="flex flex-1 flex-col">
      <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mr-2 h-4" />
        <h1 className="text-lg font-semibold">Job Posts</h1>
        <div className="ml-auto">
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            New Job Post
          </Button>
        </div>
      </header>

      <div className="flex-1 p-6">
        <div className="grid gap-6">
          {jobPosts.map((job) => (
            <Card key={job.id}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle className="text-base">{job.title}</CardTitle>
                    <p className="text-sm text-muted-foreground mt-1">Posted {job.posted}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="secondary">{job.status}</Badge>
                    <span className="text-sm text-muted-foreground">
                      {job.applicants} applicants
                    </span>
                  </div>
                </div>
              </CardHeader>

              <CardContent>
                <p className="text-sm text-muted-foreground mb-3">
                  {job.summary}
                </p>
                <div className="flex justify-end">
                 <Link href={`/job-posts/${job.id}`}>
                    <Button size="sm" variant="outline">View</Button>
                </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}




