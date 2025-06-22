import { AppSidebar } from "@/components/layout/app-sidebar"
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { SettingsContent } from "@/components/dashboard/settings-content"

export default function Settings() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <SettingsContent />
      </SidebarInset>
    </SidebarProvider>
  )
}