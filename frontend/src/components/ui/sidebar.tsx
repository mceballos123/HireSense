"use client"

import * as React from "react"
import { motion, AnimatePresence } from "framer-motion"
import { usePathname } from "next/navigation"
import Link from "next/link"
import { Home, Briefcase, Upload, Bot } from "lucide-react"

interface NavItem {
  title: string
  url: string
  icon: React.ElementType
}

const navItems: NavItem[] = [
  { title: "Dashboard", url: "/", icon: Home },
  { title: "Job Posts", url: "/job-posts", icon: Briefcase },
  { title: "Resume Uploads", url: "/resume-uploads", icon: Upload },
]

export function AppSidebar() {
  const [isExpanded, setIsExpanded] = React.useState(false)
  const [isMounted, setIsMounted] = React.useState(false)
  const pathname = usePathname()

  React.useEffect(() => {
    setIsMounted(true)
  }, [])

  const sidebarVariants = {
    expanded: {
      width: "250px",
      transition: {
        type: "spring" as const,
        stiffness: 300,
        damping: 30,
      },
    },
    collapsed: {
      width: "74px",
      transition: {
        type: "spring" as const,
        stiffness: 300,
        damping: 30,
      },
    },
  }

  return (
    <motion.div
      variants={sidebarVariants}
      animate={isExpanded ? "expanded" : "collapsed"}
      onMouseEnter={() => setIsExpanded(true)}
      onMouseLeave={() => setIsExpanded(false)}
      className="fixed top-1/2 left-4 transform -translate-y-1/2 bg-neutral-900/80 backdrop-blur-md text-white p-4 rounded-2xl shadow-lg border border-neutral-800/50 z-50 flex flex-col items-center space-y-8"
    >
      <Link href="/" passHref>
        <motion.div
          whileHover={{ scale: 1.1, rotate: 5 }}
          whileTap={{ scale: 0.95 }}
          className="cursor-pointer"
        >
          <Bot className="w-8 h-8 text-purple-400" />
        </motion.div>
      </Link>

      <motion.ul className="w-full space-y-4">
        {navItems.map((item) => (
          <li key={item.title} className="relative w-full">
            <Link href={item.url} passHref>
              <motion.div
                className="flex items-center space-x-4 p-2 rounded-lg cursor-pointer hover:bg-neutral-800/70"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.98 }}
              >
                <item.icon className="w-6 h-6 shrink-0" />
                <AnimatePresence>
                  {isExpanded && (
                    <motion.span
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -20 }}
                      transition={{ duration: 0.2, delay: 0.1 }}
                      className="whitespace-nowrap"
                    >
                      {item.title}
                    </motion.span>
                  )}
                </AnimatePresence>
              </motion.div>
            </Link>
            {isMounted && pathname === item.url && (
              <motion.div
                layoutId="active-pill"
                className="absolute inset-0 bg-purple-500/20 border border-purple-500/50 rounded-lg -z-10"
                style={{
                  boxShadow: "0 0 15px rgba(168, 85, 247, 0.5)",
                }}
                transition={{ type: "spring", stiffness: 400, damping: 35 }}
              />
            )}
          </li>
        ))}
      </motion.ul>
    </motion.div>
  )
} 