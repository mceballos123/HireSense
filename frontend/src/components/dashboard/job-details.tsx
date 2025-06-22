"use client";

import { useState, useEffect } from "react";
import { Separator } from "@/components/ui/separator";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { notFound } from "next/navigation";
import { jobPosts, detailedCandidates } from "@/lib/script";
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
import { Skeleton } from "@/components/ui/skeleton";
import { motion } from "framer-motion";

type JobDetailsProps = {
  id: string;
};

export function JobDetails({ id }: JobDetailsProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [topCandidates, setTopCandidates] = useState<any[]>([]);
  
  const job = jobPosts.find((job) => job.id.toString() === id);

  useEffect(() => {
    setIsLoading(true);
    if (job) {
      // Sort candidates by their pre-calculated overallScore
      const sortedCandidates = [...detailedCandidates].sort((a, b) => b.overallScore - a.overallScore);
      setTopCandidates(sortedCandidates);
    }
    setIsLoading(false);
  }, [id, job]);

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
            {isLoading ? (
              Array.from({ length: 4 }).map((_, index) => (
                <Card key={index} className="p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <Skeleton className="h-5 w-32" />
                    <Skeleton className="h-5 w-10" />
                  </div>
                  <Skeleton className="h-4 w-48" />
                  <div className="flex items-center gap-4 pt-1">
                    <Skeleton className="h-4 w-24" />
                    <Skeleton className="h-4 w-20" />
                  </div>
                </Card>
              ))
            ) : (
              topCandidates.map((candidate, index) => (
                <motion.div
                  key={candidate.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <Link href={`/applicant/${candidate.id}`} className="block">
                    <Card className="p-4 group hover:bg-slate-100/50 dark:hover:bg-slate-800/50 transition-colors duration-300">
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="font-bold text-slate-800 dark:text-slate-100 group-hover:text-blue-600 dark:group-hover:text-blue-400">{candidate.name}</h3>
                          <p className="text-sm text-slate-500 dark:text-slate-400">{candidate.position}</p>
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge className="bg-blue-100 text-blue-800 border-blue-300 dark:bg-blue-900/50 dark:text-blue-300 dark:border-blue-700 font-bold">
                            {candidate.overallScore}
                          </Badge>
                          <ChevronRight className="h-5 w-5 text-slate-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-transform" />
                        </div>
                      </div>
                      <Separator className="my-3" />
                      <div className="flex items-center gap-4 text-sm text-slate-500 dark:text-slate-400">
                        <div className="flex items-center gap-1.5">
                          <MapPin className="h-4 w-4" />
                          <span>{candidate.location}</span>
                        </div>
                        <div className="flex items-center gap-1.5">
                          <Clock className="h-4 w-4" />
                          <span>{candidate.experienceYears} years</span>
                        </div>
                      </div>
                    </Card>
                  </Link>
                </motion.div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}





