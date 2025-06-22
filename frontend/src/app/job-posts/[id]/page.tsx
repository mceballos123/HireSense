import { AppSidebar } from "@/components/layout/app-sidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { JobDetails } from "@/components/dashboard/job-details";

type Props = {
  params: { id: string };
};

export default function JobPostDetailPage({ params }: Props) {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <JobDetails id={params.id} />
      </SidebarInset>
    </SidebarProvider>
  );
}






