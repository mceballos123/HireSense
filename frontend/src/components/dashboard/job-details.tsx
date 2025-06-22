"use client";

import { SidebarTrigger } from "@/components/ui/sidebar";
import { Separator } from "@/components/ui/separator";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { notFound } from "next/navigation";
import { jobPosts } from "@/lib/script";
import Link from "next/link";
import { ArrowLeft, Briefcase, Calendar, Users, Star, CheckCircle, Target } from "lucide-react";

type JobDetailsProps = {
  id: string;
};

export function JobDetails({ id }: JobDetailsProps) {
  const job = jobPosts.find((job) => job.id.toString() === id);

  if (!job) return notFound();

  return (
    <div className="flex flex-1 flex-col bg-gradient-to-br from-slate-50 via-white to-blue-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-blue-950/20">
      {/* Top nav bar */}
      <header className="flex h-20 items-center gap-3 border-b border-white/20 bg-white/70 backdrop-blur-xl px-8 shadow-sm dark:bg-slate-900/70 dark:border-slate-800/50">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mr-3 h-6" />
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-violet-600">
            <Briefcase className="h-4 w-4 text-white" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 via-blue-800 to-violet-800 bg-clip-text text-transparent dark:from-white dark:via-blue-200 dark:to-violet-200">
            Job Description
          </h1>
        </div>
        <div className="ml-auto">
          <Link href="/job-posts">
            <Button variant="ghost" size="sm" className="gap-2 hover:bg-slate-100 dark:hover:bg-slate-800">
              <ArrowLeft className="h-4 w-4" />
              Back to Job Posts
            </Button>
          </Link>
        </div>
      </header>

      {/* Page content */}
      <div className="flex-1 p-8 space-y-8">
        {/* Job Header */}
        <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm dark:bg-slate-800/90 dark:border-slate-700/60">
          <CardContent className="p-8">
            <div className="flex items-start justify-between">
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="p-3 rounded-lg bg-gradient-to-br from-blue-600 to-violet-600">
                    <Briefcase className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <h2 className="text-3xl font-bold text-slate-900 dark:text-white">{job.title}</h2>
                    <div className="flex items-center gap-4 mt-2 text-sm text-slate-600 dark:text-slate-400">
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
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Badge className="bg-gradient-to-r from-emerald-500 to-teal-500 text-white border-0 shadow-lg shadow-emerald-500/20">
                  {job.status}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Description */}
        <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm hover:shadow-md transition-shadow dark:bg-slate-800/90 dark:border-slate-700/60">
          <CardHeader className="pb-6">
            <CardTitle className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <div className="p-2 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500">
                <Target className="h-4 w-4 text-white" />
              </div>
              Job Description
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-base leading-relaxed text-slate-700 dark:text-slate-300">{job.description}</p>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Responsibilities */}
          <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm hover:shadow-md transition-shadow dark:bg-slate-800/90 dark:border-slate-700/60">
            <CardHeader className="pb-6">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-gradient-to-br from-amber-500 to-orange-500">
                  <Star className="h-4 w-4 text-white" />
                </div>
                <div>
                  <CardTitle className="text-xl font-bold text-slate-900 dark:text-white">Key Responsibilities</CardTitle>
                  <p className="text-slate-600 dark:text-slate-400">What you'll be doing</p>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {job.responsibilities.map((item, index) => (
                  <li key={index} className="flex items-start gap-3 text-slate-700 dark:text-slate-300">
                    <div className="mt-1.5 h-2 w-2 rounded-full bg-gradient-to-r from-amber-500 to-orange-500 flex-shrink-0" />
                    <span className="leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          {/* Qualifications */}
          <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm hover:shadow-md transition-shadow dark:bg-slate-800/90 dark:border-slate-700/60">
            <CardHeader className="pb-6">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-500">
                  <CheckCircle className="h-4 w-4 text-white" />
                </div>
                <div>
                  <CardTitle className="text-xl font-bold text-slate-900 dark:text-white">Requirements</CardTitle>
                  <p className="text-slate-600 dark:text-slate-400">What we're looking for</p>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {job.qualifications.map((item, index) => (
                  <li key={index} className="flex items-start gap-3 text-slate-700 dark:text-slate-300">
                    <div className="mt-1.5 h-2 w-2 rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 flex-shrink-0" />
                    <span className="leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </div>

        {/* Bonus */}
        <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm hover:shadow-md transition-shadow dark:bg-slate-800/90 dark:border-slate-700/60">
          <CardHeader className="pb-6">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-gradient-to-br from-violet-500 to-purple-500">
                <Star className="h-4 w-4 text-white" />
              </div>
              <div>
                <CardTitle className="text-xl font-bold text-slate-900 dark:text-white">Nice to Have</CardTitle>
                <p className="text-slate-600 dark:text-slate-400">Bonus qualifications</p>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3">
              {job.bonus.map((item, index) => (
                <li key={index} className="flex items-start gap-3 text-slate-700 dark:text-slate-300">
                  <div className="mt-1.5 h-2 w-2 rounded-full bg-gradient-to-r from-violet-500 to-purple-500 flex-shrink-0" />
                  <span className="leading-relaxed">{item}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        {/* Technologies */}
        {job.technologies?.length > 0 && (
          <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm hover:shadow-md transition-shadow dark:bg-slate-800/90 dark:border-slate-700/60">
            <CardHeader>
              <CardTitle className="text-xl font-bold text-slate-900 dark:text-white">Tech Stack</CardTitle>
              <p className="text-slate-600 dark:text-slate-400">Technologies you'll work with</p>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-3">
                {job.technologies.map((tech) => (
                  <Badge
                    key={tech}
                    className="px-4 py-2 text-sm font-medium bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 text-white border-0 shadow-sm transition-all hover:shadow-md"
                  >
                    {tech}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Apply Section */}
        <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm dark:bg-slate-800/90 dark:border-slate-700/60">
          <CardContent className="p-8">
            <div className="text-center space-y-4">
              <h3 className="text-2xl font-bold text-slate-900 dark:text-white">Ready to Apply?</h3>
              <p className="text-slate-600 dark:text-slate-400">Join our team and make an impact</p>
              <div className="flex items-center justify-center gap-4">
                <Button className="px-8 py-3 bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 text-white border-0 shadow-lg shadow-blue-500/25 font-semibold">
                  Apply for this Role
                </Button>
                <Button variant="outline" className="px-8 py-3 border-slate-300 hover:bg-slate-50 dark:border-slate-600 dark:hover:bg-slate-800">
                  Save for Later
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}





