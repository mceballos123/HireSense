import { AppSidebar } from "@/components/layout/app-sidebar"
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { ApplicantAnalysis } from "@/components/dashboard/applicant-analysis"

export default async function ApplicantPage({
  params,
}: {
  params: { id: string }
}) {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <ApplicantAnalysis applicantId={params.id} />
      </SidebarInset>
    </SidebarProvider>
  )
}
