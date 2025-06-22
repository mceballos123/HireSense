import { AppSidebar } from "@/components/layout/app-sidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { JobDetails } from "@/components/dashboard/job-details";

type Props = {
  params: Promise<{ id: string }>;
};

export default async function JobPostDetailPage({ params }: Props) {
  const { id } = await params;
  
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <JobDetails id={id} />
      </SidebarInset>
    </SidebarProvider>
  );
}






