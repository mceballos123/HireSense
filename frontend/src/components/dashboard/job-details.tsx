"use client";

import { Separator } from "@/components/ui/separator";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { notFound } from "next/navigation";
import { jobPosts, applicants } from "@/lib/script";
import Link from "next/link";
import {
  ArrowLeft,
  Briefcase,
  Calendar,
  Users,
  Star,
  CheckCircle,
  Target,
  Clock,
  MapPin,
  ChevronRight,
  Zap
} from "lucide-react";

type JobDetailsProps = {
  id: string;
};

// Helper function from dashboard-content
const getScoreColor = (score: number) => {
  if (score >= 90) return "text-emerald-600 dark:text-emerald-400";
  if (score >= 80) return "text-blue-600 dark:text-blue-400";
  if (score >= 70) return "text-amber-600 dark:text-amber-400";
  return "text-slate-600 dark:text-slate-400";
};

export function JobDetails({ id }: JobDetailsProps) {
  const job = jobPosts.find((job) => job.id.toString() === id);
  const sortedApplicants = [...applicants].sort((a, b) => b.score - a.score);

  if (!job) return notFound();

  return (
    <div className="flex flex-1 flex-col bg-gradient-to-br from-slate-50 via-white to-blue-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-blue-950/20">
      <header className="flex h-20 items-center gap-3 border-b border-white/20 bg-white/70 backdrop-blur-xl px-8 shadow-sm dark:bg-slate-900/70 dark:border-slate-800/50">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-violet-600">
            <Briefcase className="h-4 w-4 text-white" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 via-blue-800 to-violet-800 bg-clip-text text-transparent dark:from-white dark:via-blue-200 dark:to-violet-200">
            {job.title}
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

      <div className="flex-1 p-8 grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        {/* Left column for job details */}
        <div className="lg:col-span-2 space-y-8">
          {/* Job Description */}
          <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm dark:bg-slate-800/90 dark:border-slate-700/60">
            <CardHeader>
              <CardTitle className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Target className="h-5 w-5 text-blue-500" />
                Job Description
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-base leading-relaxed text-slate-700 dark:text-slate-300">{job.description}</p>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Responsibilities */}
            <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm dark:bg-slate-800/90 dark:border-slate-700/60">
              <CardHeader>
                <CardTitle className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                  <Star className="h-5 w-5 text-amber-500" />
                  Key Responsibilities
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {job.responsibilities.map((item, index) => (
                    <li key={index} className="flex items-start gap-3 text-slate-700 dark:text-slate-300">
                      <div className="mt-1.5 h-2 w-2 rounded-full bg-amber-500 flex-shrink-0" />
                      <span className="leading-relaxed">{item}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            {/* Qualifications */}
            <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm dark:bg-slate-800/90 dark:border-slate-700/60">
              <CardHeader>
                <CardTitle className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-emerald-500" />
                  Requirements
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {job.qualifications.map((item, index) => (
                    <li key={index} className="flex items-start gap-3 text-slate-700 dark:text-slate-300">
                      <div className="mt-1.5 h-2 w-2 rounded-full bg-emerald-500 flex-shrink-0" />
                      <span className="leading-relaxed">{item}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Right column for applicants */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Top Candidates</h2>
              <p className="text-slate-600 dark:text-slate-400">AI-ranked applicants for this role</p>
            </div>
          </div>
          <div className="space-y-4">
            {sortedApplicants.map((applicant) => (
              <Card key={applicant.id} className="group relative overflow-hidden border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm hover:shadow-lg hover:border-blue-300/60 transition-all duration-300 hover:-translate-y-0.5 dark:bg-slate-800/90 dark:border-slate-700/60 dark:hover:border-blue-600/60">
                <div className="absolute top-4 right-4">
                  <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gradient-to-r from-blue-50 to-violet-50 border border-blue-200/50 dark:from-blue-950/50 dark:to-violet-950/50 dark:border-blue-800/30">
                    <Zap className="h-3.5 w-3.5 text-blue-600 dark:text-blue-400" />
                    <span className={`text-sm font-bold ${getScoreColor(applicant.score)}`}>
                      {applicant.score}
                    </span>
                  </div>
                </div>
                <CardContent className="p-6 pr-20">
                  <div className="space-y-3">
                    <div>
                      <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                        {applicant.name}
                      </h3>
                      <p className="text-base text-slate-600 dark:text-slate-400 font-medium">{applicant.position}</p>
                    </div>
                    <div className="flex items-center gap-4 text-xs text-slate-500 dark:text-slate-400">
                      <div className="flex items-center gap-1.5">
                        <MapPin className="h-3.5 w-3.5" />
                        <span>{applicant.location}</span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <Clock className="h-3.5 w-3.5" />
                        <span>{applicant.experience}</span>
                      </div>
                    </div>
                    <div className="transition-all duration-300 max-h-0 group-hover:max-h-12 group-hover:pt-2 overflow-hidden">
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
      </div>
    </div>
  );
}





