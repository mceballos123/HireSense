import { AppSidebar } from "@/components/layout/app-sidebar"
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { JobPostsContent } from "@/components/dashboard/job-posts-content"

export default function JobPosts() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <JobPostsContent />
      </SidebarInset>
    </SidebarProvider>
  )
}