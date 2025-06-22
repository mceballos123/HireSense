import { ApplicantAnalysis } from "@/components/dashboard/applicant-analysis"

export default function ApplicantPage({ params }: { params: { id: string } }) {
  return <ApplicantAnalysis applicantId={params.id} />
}
