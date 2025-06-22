import { AppSidebar } from "@/components/layout/app-sidebar"
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { ApplicantAnalysis } from "@/components/dashboard/applicant-analysis"

export default async function ApplicantPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params;
  
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <ApplicantAnalysis applicantId={id} />
      </SidebarInset>
    </SidebarProvider>
  )
}
