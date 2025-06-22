import { JobDetails } from "@/components/dashboard/job-details"

export default function JobDetailsPage({
  params,
}: {
  params: { id: string }
}) {
  return <JobDetails id={params.id} />
}






