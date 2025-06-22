"use client";

import { SidebarTrigger } from "@/components/ui/sidebar";
import { Separator } from "@/components/ui/separator";
import { notFound } from "next/navigation";
import { jobPosts } from "@/lib/script";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

type JobDetailsProps = {
  id: string;
};

export function JobDetails({ id }: JobDetailsProps) {
  const job = jobPosts.find((job) => job.id.toString() === id);

  if (!job) return notFound();

  return (
    <div className="flex flex-1 flex-col">
      {/* Top nav bar */}
      <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mr-2 h-4" />
        <h1 className="text-lg font-semibold">Job Description</h1>
      </header>

      {/* Page content */}
      <div className="flex-1 px-6 py-8 space-y-6">
        {/* Job Title + Meta */}
        <section className="space-y-1">
          <h2 className="text-2xl font-bold">{job.title}</h2>
          <p className="text-sm text-muted-foreground">Posted {job.posted}</p>
        </section>

        {/* Description */}
        <section className="space-y-3">
          <h3 className="text-lg font-semibold">Description</h3>
          <p className="text-base leading-relaxed">{job.description}</p>
        </section>

        {/* Responsibilities */}
        <section className="space-y-3">
          <h3 className="text-lg font-semibold">Responsibilities</h3>
          <ul className="list-disc list-inside space-y-1">
            {job.responsibilities.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>

        {/* Qualifications */}
        <section className="space-y-3">
          <h3 className="text-lg font-semibold">Qualifications</h3>
          <ul className="list-disc list-inside space-y-1">
            {job.qualifications.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>

        {/* Bonus */}
        <section className="space-y-3">
          <h3 className="text-lg font-semibold">Bonus</h3>
          <ul className="list-disc list-inside space-y-1">
            {job.bonus.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>

        {/* Technologies */}
        {job.technologies?.length > 0 && (
          <section className="space-y-3">
            <h3 className="text-lg font-semibold">Technologies</h3>
            <div className="flex flex-wrap gap-2">
              {job.technologies.map((tech) => (
                <span
                  key={tech}
                  className="rounded-full border border-muted px-3 py-1 text-sm text-muted-foreground bg-background/40 hover:bg-background transition"
                >
                  {tech}
                </span>
              ))}
            </div>
          </section>
        )}

        {/* Back Button */}
        <div className="pt-6">
          <Link href="/job-posts" className="inline-flex items-center text-sm font-medium hover:underline text-muted-foreground">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Job Posts
          </Link>
        </div>
      </div>
    </div>
  );
}





