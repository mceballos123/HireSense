"use client"

import { useState, useEffect, useRef } from "react"
import { CheckCircle, XCircle, Target, Scale, BrainCircuit, Loader2 } from "lucide-react"

interface AgentEvent {
  type: string
  agent_name: string
  message: string
  step: string
  position: string
  timestamp: number
}

export function AnalysisInProgress() {
  const [events, setEvents] = useState<AgentEvent[]>([])
  const [isConnected, setIsConnected] = useState(false)
  const [currentStep, setCurrentStep] = useState("Initializing...")
  const eventsEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new events are added
  const scrollToBottom = () => {
    eventsEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [events])

  useEffect(() => {
    // Try to connect to WebSocket, with fallback for different ports
    const connectWebSocket = () => {
      const ws = new WebSocket('ws://localhost:8081/ws/progress')
      
      ws.onopen = () => {
        setIsConnected(true)
        console.log('WebSocket connected to port 8080')
      }
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data) as AgentEvent
        console.log('Received event:', data)
        
        setEvents(prev => [...prev, data])
        
        // Update current step based on the event
        if (data.step === "initialization") setCurrentStep("Initializing agents...")
        else if (data.step === "parsing") setCurrentStep("Analyzing job and resume...")
        else if (data.step === "evaluation") setCurrentStep("Evaluating candidate-job fit...")
        else if (data.step === "debate") setCurrentStep("AI agents debating hiring decision...")
        else if (data.step === "decision") setCurrentStep("Making final decision...")
        else if (data.step === "completed") setCurrentStep("Analysis complete!")
      }
      
      ws.onclose = () => {
        setIsConnected(false)
        console.log('WebSocket disconnected')
      }
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        setIsConnected(false)
      }
      
      return ws
    }

    const ws = connectWebSocket()
    
    return () => {
      ws.close()
    }
  }, [])

  const getAgentIcon = (agentName: string, position: string) => {
    if (agentName === "Intersection Evaluator") return <Target className="h-5 w-5 text-blue-500" />
    if (agentName === "Pro-Hire Advocate") return <CheckCircle className="h-5 w-5 text-emerald-500" />
    if (agentName === "Anti-Hire Advocate") return <XCircle className="h-5 w-5 text-red-500" />
    if (agentName === "Decision Agent") return <Scale className="h-5 w-5 text-violet-500" />
    return <BrainCircuit className="h-5 w-5 text-slate-500" />
  }

  const getEventBgColor = (agentName: string, position: string) => {
    if (position === "evaluation") return "bg-blue-50 dark:bg-blue-900/30 border-blue-200 dark:border-blue-800"
    if (position === "pro") return "bg-emerald-50 dark:bg-emerald-900/30 border-emerald-200 dark:border-emerald-800"
    if (position === "anti") return "bg-red-50 dark:bg-red-900/30 border-red-200 dark:border-red-800"
    if (agentName === "Decision Agent") return "bg-violet-50 dark:bg-violet-900/30 border-violet-200 dark:border-violet-800"
    return "bg-slate-50 dark:bg-slate-800/50 border-slate-200 dark:border-slate-700"
  }

  const getAgentNameColor = (agentName: string, position: string) => {
    if (position === "evaluation") return "text-blue-600 dark:text-blue-400"
    if (position === "pro") return "text-emerald-600 dark:text-emerald-400"
    if (position === "anti") return "text-red-600 dark:text-red-400"
    if (agentName === "Decision Agent") return "text-violet-600 dark:text-violet-400"
    return "text-slate-600 dark:text-slate-400"
  }

  return (
    <div className="flex flex-1 flex-col bg-gradient-to-br from-slate-50 via-white to-blue-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-blue-950/20">
      {/* Header */}
      <div className="text-center py-8 border-b border-slate-200 dark:border-slate-700">
        <div className="flex items-center justify-center gap-3 mb-4">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
          <h2 className="text-3xl font-bold bg-gradient-to-r from-slate-900 via-blue-800 to-violet-800 bg-clip-text text-transparent dark:from-white dark:via-blue-200 dark:to-violet-200">
            AI Agents at Work
          </h2>
        </div>
        <p className="text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
          Watch our team of specialized AI agents collaborate to evaluate this candidate
        </p>
        <div className="mt-4">
          <p className="text-sm font-medium text-slate-700 dark:text-slate-300">
            Current Step: {currentStep}
          </p>
          <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            {isConnected ? "🟢 Connected" : "🔴 Disconnected"}
          </div>
        </div>
      </div>

      {/* Agent Events Stream */}
      <div className="flex-1 p-8 overflow-y-auto">
        <div className="max-w-4xl mx-auto space-y-4">
          {events.length === 0 ? (
            <div className="text-center py-12">
              <BrainCircuit className="h-12 w-12 mx-auto text-slate-400 mb-4" />
              <p className="text-slate-500 dark:text-slate-400">
                Waiting for agents to start working...
              </p>
            </div>
          ) : (
            events.map((event, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg border transition-all duration-300 ${getEventBgColor(event.agent_name, event.position)}`}
              >
                <div className="flex items-start gap-3">
                  <div className="mt-0.5">
                    {getAgentIcon(event.agent_name, event.position)}
                  </div>
                  <div className="flex-1">
                    <h4 className={`font-semibold text-sm ${getAgentNameColor(event.agent_name, event.position)}`}>
                      {event.agent_name}
                      {event.position === "pro" && ` (Round ${Math.ceil(events.filter(e => e.position === "pro").length)})`}
                      {event.position === "anti" && ` (Round ${events.filter(e => e.position === "anti").length})`}
                    </h4>
                    <p className="text-slate-700 dark:text-slate-300 mt-1 leading-relaxed">
                      {event.message}
                    </p>
                    <div className="text-xs text-slate-500 dark:text-slate-400 mt-2">
                      {new Date(event.timestamp * 1000).toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
          {/* Invisible element at the bottom for auto-scroll */}
          <div ref={eventsEndRef} />
        </div>
      </div>
    </div>
  )
} 