// app/resume-uploads/page.tsx
import { AppSidebar } from "@/components/layout/app-sidebar"
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"
import { ResumeUploadsContent } from "@/components/dashboard/resume-uploads-content"

export default function ResumeUploadsPage() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <ResumeUploadsContent />
      </SidebarInset>
    </SidebarProvider>
  )
}
