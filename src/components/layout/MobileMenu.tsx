import React from 'react'
import { Link, useLocation } from '@tanstack/react-router'
import { motion } from 'framer-motion'
import { NavItem } from '@/types'

interface MobileMenuProps {
  onClose: () => void
}

function MobileMenu({ onClose }: MobileMenuProps) {
  const location = useLocation()
  const [expandedItems, setExpandedItems] = React.useState<string[]>([])

  const navigationItems: NavItem[] = [
    { label: 'MATCHES', href: '/matches' },
    { 
      label: 'POINTS TABLE', 
      href: '/stats',
      children: [
        { label: 'Overall Stats', href: '/stats' },
        { label: 'Head to Head', href: '/stats/head-to-head' }
      ]
    },
    { 
      label: 'VIDEOS', 
      href: '/videos',
      children: [
        { label: 'Latest', href: '/videos' },
        { label: 'BCL Exclusive', href: '/videos/exclusive' },
        { label: 'Magic Moments', href: '/videos/magic-moments' },
        { label: 'Highlights', href: '/videos/highlights' },
        { label: 'Interviews', href: '/videos/interviews' },
        { label: 'Press Conferences', href: '/videos/press-conferences' }
      ]
    },
    { label: 'TEAMS', href: '/teams' },
    { 
      label: 'NEWS', 
      href: '/news',
      children: [
        { label: 'All News', href: '/news' },
        { label: 'Announcements', href: '/news/announcements' },
        { label: 'Match Reports', href: '/news/match-reports' }
      ]
    },
    { label: 'FANTASY', href: '/fantasy' },
    { 
      label: 'STATS', 
      href: '/stats',
      children: [
        { label: 'Overall Stats', href: '/stats' },
        { label: 'Head to Head', href: '/stats/head-to-head' }
      ]
    },
    { 
      label: 'MORE', 
      href: '#',
      children: [
        { label: 'Fan Contests', href: '/fan-contests' },
        { label: 'Photos', href: '/photos' },
        { label: 'Mobile Products', href: '/mobile' },
        { label: 'Venues', href: '/venues' },
        { label: 'About', href: '/about' }
      ]
    }
  ]

  const toggleExpanded = (label: string) => {
    setExpandedItems(prev => 
      prev.includes(label) 
        ? prev.filter(item => item !== label)
        : [...prev, label]
    )
  }

  const isActive = (href: string) => {
    return location.pathname === href || location.pathname.startsWith(href + '/')
  }

  return (
    <motion.div
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: 'auto' }}
      exit={{ opacity: 0, height: 0 }}
      className="lg:hidden bg-white border-t border-gray-200 shadow-lg"
    >
      <div className="px-2 pt-2 pb-3 space-y-1">
        {navigationItems.map((item, index) => (
          <motion.div
            key={item.label}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <div>
              <div className="flex items-center justify-between">
                <Link
                  to={item.href}
                  onClick={onClose}
                  className={`block px-3 py-2 text-base font-medium rounded-md transition-colors duration-200 ${
                    isActive(item.href)
                      ? 'text-primary-green bg-gray-50'
                      : 'text-gray-700 hover:text-primary-green hover:bg-gray-50'
                  }`}
                >
                  {item.label}
                </Link>
                
                {item.children && (
                  <button
                    onClick={() => toggleExpanded(item.label)}
                    className="p-2 text-gray-500 hover:text-primary-green"
                  >
                    <motion.svg
                      animate={{ rotate: expandedItems.includes(item.label) ? 180 : 0 }}
                      transition={{ duration: 0.2 }}
                      className="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 9l-7 7-7-7"
                      />
                    </motion.svg>
                  </button>
                )}
              </div>

              {/* Submenu */}
              {item.children && expandedItems.includes(item.label) && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="ml-4 space-y-1"
                >
                  {item.children.map((child, childIndex) => (
                    <motion.div
                      key={child.href}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: childIndex * 0.05 }}
                    >
                      <Link
                        to={child.href}
                        onClick={onClose}
                        className="block px-3 py-2 text-sm text-gray-600 hover:text-primary-green hover:bg-gray-50 rounded-md transition-colors duration-200"
                      >
                        {child.label}
                      </Link>
                    </motion.div>
                  ))}
                </motion.div>
              )}
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  )
}

export default MobileMenu
