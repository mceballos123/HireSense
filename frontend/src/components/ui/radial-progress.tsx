"use client"

import * as React from "react"

interface RadialProgressProps extends React.SVGProps<SVGSVGElement> {
  value: number // 0 to 100
  strokeWidth?: number
}

export function RadialProgress({
  value,
  strokeWidth = 10,
  className,
  ...props
}: RadialProgressProps) {
  const radius = 50 - strokeWidth / 2
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (value / 100) * circumference

  return (
    <svg
      viewBox="0 0 100 100"
      className={className}
      {...props}
    >
      <circle
        className="text-slate-200 dark:text-slate-700"
        stroke="currentColor"
        strokeWidth={strokeWidth}
        fill="transparent"
        r={radius}
        cx="50"
        cy="50"
      />
      <circle
        className="text-emerald-500"
        stroke="currentColor"
        strokeWidth={strokeWidth}
        fill="transparent"
        strokeLinecap="round"
        r={radius}
        cx="50"
        cy="50"
        style={{
          strokeDasharray: circumference,
          strokeDashoffset: strokeDashoffset,
          transform: "rotate(-90deg)",
          transformOrigin: "50% 50%",
          transition: "stroke-dashoffset 0.5s ease-out",
        }}
      />
      <text
        x="50"
        y="50"
        textAnchor="middle"
        dy=".3em"
        className="text-2xl font-bold fill-slate-800 dark:fill-slate-200"
      >
        {`${Math.round(value)}%`}
      </text>
    </svg>
  )
} 