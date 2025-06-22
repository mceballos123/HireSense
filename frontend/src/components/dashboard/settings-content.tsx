"use client"

import { Settings, User, Brain, Shield } from "lucide-react"
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
    <div className="flex flex-1 flex-col bg-gradient-to-br from-slate-50 via-white to-blue-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-blue-950/20">
      <header className="flex h-20 items-center gap-3 border-b border-white/20 bg-white/70 backdrop-blur-xl px-8 shadow-sm dark:bg-slate-900/70 dark:border-slate-800/50">
        <SidebarTrigger className="-ml-1" />
        <Separator orientation="vertical" className="mr-3 h-6" />
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-600 to-violet-600">
            <Settings className="h-4 w-4 text-white" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 via-blue-800 to-violet-800 bg-clip-text text-transparent dark:from-white dark:via-blue-200 dark:to-violet-200">
            Settings
          </h1>
        </div>
      </header>

      <div className="flex-1 p-8 space-y-8">
        {/* Profile Settings */}
        <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm hover:shadow-md transition-shadow dark:bg-slate-800/90 dark:border-slate-700/60">
          <CardHeader className="pb-6">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-500">
                <User className="h-5 w-5 text-white" />
              </div>
              <div>
                <CardTitle className="text-xl font-bold text-slate-900 dark:text-white">Profile Settings</CardTitle>
                <p className="text-slate-600 dark:text-slate-400">Update your personal information</p>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="firstName" className="text-sm font-medium text-slate-700 dark:text-slate-300">
                  First Name
                </Label>
                <Input 
                  id="firstName" 
                  placeholder="Enter your first name" 
                  className="border-slate-200/60 bg-white/50 focus:border-blue-500 focus:ring-blue-500/20 dark:border-slate-700/60 dark:bg-slate-800/50"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="lastName" className="text-sm font-medium text-slate-700 dark:text-slate-300">
                  Last Name
                </Label>
                <Input 
                  id="lastName" 
                  placeholder="Enter your last name" 
                  className="border-slate-200/60 bg-white/50 focus:border-blue-500 focus:ring-blue-500/20 dark:border-slate-700/60 dark:bg-slate-800/50"
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="email" className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Email
              </Label>
              <Input 
                id="email" 
                type="email" 
                placeholder="Enter your email" 
                className="border-slate-200/60 bg-white/50 focus:border-blue-500 focus:ring-blue-500/20 dark:border-slate-700/60 dark:bg-slate-800/50"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="company" className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Company
              </Label>
              <Input 
                id="company" 
                placeholder="Enter your company name" 
                className="border-slate-200/60 bg-white/50 focus:border-blue-500 focus:ring-blue-500/20 dark:border-slate-700/60 dark:bg-slate-800/50"
              />
            </div>
          </CardContent>
        </Card>

        {/* AI Settings */}
        <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm hover:shadow-md transition-shadow dark:bg-slate-800/90 dark:border-slate-700/60">
          <CardHeader className="pb-6">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-gradient-to-br from-violet-500 to-purple-500">
                <Brain className="h-5 w-5 text-white" />
              </div>
              <div>
                <CardTitle className="text-xl font-bold text-slate-900 dark:text-white">AI Evaluation Settings</CardTitle>
                <p className="text-slate-600 dark:text-slate-400">Configure how AI processes applications</p>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center justify-between p-4 rounded-lg border border-slate-200/50 bg-slate-50/50 dark:border-slate-700/50 dark:bg-slate-800/50">
              <div className="space-y-1">
                <Label className="text-slate-900 dark:text-white font-medium">Auto-evaluate new applications</Label>
                <p className="text-sm text-slate-600 dark:text-slate-400">Automatically run AI evaluation on new applicants</p>
              </div>
              <Switch />
            </div>
            <div className="flex items-center justify-between p-4 rounded-lg border border-slate-200/50 bg-slate-50/50 dark:border-slate-700/50 dark:bg-slate-800/50">
              <div className="space-y-1">
                <Label className="text-slate-900 dark:text-white font-medium">Email notifications</Label>
                <p className="text-sm text-slate-600 dark:text-slate-400">Get notified when high-scoring candidates apply</p>
              </div>
              <Switch />
            </div>
            <div className="space-y-2">
              <Label htmlFor="scoreThreshold" className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Minimum score threshold for notifications
              </Label>
              <Input 
                id="scoreThreshold" 
                type="number" 
                placeholder="85" 
                className="border-slate-200/60 bg-white/50 focus:border-blue-500 focus:ring-blue-500/20 dark:border-slate-700/60 dark:bg-slate-800/50"
              />
            </div>
          </CardContent>
        </Card>

        {/* Custom Evaluation Criteria */}
        <Card className="border border-slate-200/60 bg-white/90 backdrop-blur-sm shadow-sm hover:shadow-md transition-shadow dark:bg-slate-800/90 dark:border-slate-700/60">
          <CardHeader className="pb-6">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-gradient-to-br from-amber-500 to-orange-500">
                <Shield className="h-5 w-5 text-white" />
              </div>
              <div>
                <CardTitle className="text-xl font-bold text-slate-900 dark:text-white">Custom Evaluation Criteria</CardTitle>
                <p className="text-slate-600 dark:text-slate-400">Define specific requirements for candidate evaluation</p>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="criteria" className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Additional evaluation criteria
              </Label>
              <Textarea
                id="criteria"
                placeholder="Enter any specific criteria you want the AI to consider when evaluating candidates..."
                rows={4}
                className="border-slate-200/60 bg-white/50 focus:border-blue-500 focus:ring-blue-500/20 dark:border-slate-700/60 dark:bg-slate-800/50"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="keywords" className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Required keywords
              </Label>
              <Input 
                id="keywords" 
                placeholder="React, TypeScript, Node.js (comma separated)" 
                className="border-slate-200/60 bg-white/50 focus:border-blue-500 focus:ring-blue-500/20 dark:border-slate-700/60 dark:bg-slate-800/50"
              />
            </div>
          </CardContent>
        </Card>

        {/* Save Button */}
        <div className="flex justify-end">
          <Button className="px-8 py-3 bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 text-white border-0 shadow-lg shadow-blue-500/25 font-semibold">
            Save Settings
          </Button>
        </div>
      </div>
    </div>
  )
}