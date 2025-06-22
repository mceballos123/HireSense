"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Switch } from "@/components/ui/switch"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { Textarea } from "@/components/ui/textarea"

export function SettingsContent() {
  return (
    <div className="flex flex-1 flex-col">
      <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mr-2 h-4" />
        <h1 className="text-lg font-semibold">Settings</h1>
      </header>

      <div className="flex-1 p-6 space-y-6">
        {/* Profile Settings */}
        <Card>
          <CardHeader>
            <CardTitle>Profile Settings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="firstName">First Name</Label>
                <Input id="firstName" placeholder="Enter your first name" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="lastName">Last Name</Label>
                <Input id="lastName" placeholder="Enter your last name" />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" placeholder="Enter your email" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="company">Company</Label>
              <Input id="company" placeholder="Enter your company name" />
            </div>
          </CardContent>
        </Card>

        {/* AI Settings */}
        <Card>
          <CardHeader>
            <CardTitle>AI Evaluation Settings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Auto-evaluate new applications</Label>
                <p className="text-sm text-muted-foreground">Automatically run AI evaluation on new applicants</p>
              </div>
              <Switch />
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Email notifications</Label>
                <p className="text-sm text-muted-foreground">Get notified when high-scoring candidates apply</p>
              </div>
              <Switch />
            </div>
            <div className="space-y-2">
              <Label htmlFor="scoreThreshold">Minimum score threshold for notifications</Label>
              <Input id="scoreThreshold" type="number" placeholder="85" />
            </div>
          </CardContent>
        </Card>

        {/* Custom Evaluation Criteria */}
        <Card>
          <CardHeader>
            <CardTitle>Custom Evaluation Criteria</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="criteria">Additional evaluation criteria</Label>
              <Textarea
                id="criteria"
                placeholder="Enter any specific criteria you want the AI to consider when evaluating candidates..."
                rows={4}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="keywords">Required keywords</Label>
              <Input id="keywords" placeholder="React, TypeScript, Node.js (comma separated)" />
            </div>
          </CardContent>
        </Card>

        {/* Save Button */}
        <div className="flex justify-end">
          <Button>Save Settings</Button>
        </div>
      </div>
    </div>
  )
}