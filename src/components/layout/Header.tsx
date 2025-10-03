import React, { useState } from 'react'
import { Link, useLocation } from '@tanstack/react-router'
import { motion } from 'framer-motion'
import { NavItem } from '@/types'
// import BCLogo from '@/assets/images/BCL BELLANDUR CRICKET.png'

interface HeaderProps {
  isMobileMenuOpen: boolean
  onMobileMenuToggle: () => void
}

function Header({ isMobileMenuOpen, onMobileMenuToggle }: HeaderProps) {
  const location = useLocation()
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null)

  const navigationItems: NavItem[] = [
    { label: 'MATCHES', href: '/matches' },
    { label: 'POINTS TABLE', href: '/stats' },
    { 
      label: 'VIDEOS', 
      href: '/videos',
      children: [
        { label: 'LATEST', href: '/videos' },
        { label: 'BCL EXCLUSIVE', href: '/videos/exclusive' },
        { label: 'MAGIC MOMENTS', href: '/videos/magic-moments' },
        { label: 'HIGHLIGHTS', href: '/videos/highlights' },
        { label: 'INTERVIEWS', href: '/videos/interviews' },
        { label: 'PRESS CONFERENCES', href: '/videos/press-conferences' },
        { label: 'ALL', href: '/videos/all' }
      ]
    },
    { 
      label: 'TEAMS', 
      href: '/teams',
      children: [
        { label: 'All Teams', href: '/teams' },
        { label: 'MR Titans', href: '/teams/mr-titans' },
        { label: 'Bellandur Monsters', href: '/teams/bellandur-monsters' },
        { label: 'YKR Cricketers', href: '/teams/ykr-cricketers' },
        { label: 'Bellandur Sharks', href: '/teams/bellandur-sharks' },
        { label: 'Super Giants', href: '/teams/super-giants' },
        { label: 'Royal Changlesrs', href: '/teams/royal-changlesrs' }
      ]
    },
    { 
      label: 'NEWS', 
      href: '/news',
      children: [
        { label: 'ALL NEWS', href: '/news' },
        { label: 'ANNOUNCEMENTS', href: '/news/announcements' },
        { label: 'MATCH REPORTS', href: '/news/match-reports' }
      ]
    },
    { label: 'FANTASY', href: '/fantasy' },
    { 
      label: 'STATS', 
      href: '/stats',
      children: [
        { label: 'OVERALL STATS', href: '/stats' },
        { label: 'HEAD TO HEAD', href: '/stats/head-to-head' }
      ]
    },
    { 
      label: 'MORE', 
      href: '#',
      children: [
        { label: 'FAN CONTESTS', href: '/fan-contests' },
        { label: 'PHOTOS', href: '/photos' },
        { label: 'MOBILE PRODUCTS', href: '/mobile' },
        { label: 'VENUES', href: '/venues' },
        { label: 'AUCTION', href: '/auction' },
        { label: 'ABOUT', href: '/about' }
      ]
    }
  ]

  const isActive = (href: string) => {
    return location.pathname === href || location.pathname.startsWith(href + '/')
  }

  return (
    <header className="bg-blue-900 shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center">
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center"
            >
              <div className="w-12 h-12 bg-cricket-green rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-lg">BCL</span>
              </div>
            </motion.div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            {navigationItems.map((item) => (
              <div
                key={item.label}
                className="relative"
                onMouseEnter={() => setActiveDropdown(item.label)}
                onMouseLeave={() => setActiveDropdown(null)}
              >
                <Link
                  to={item.href}
                  className={`px-3 py-2 text-xs font-medium transition-colors duration-200 ${
                    isActive(item.href)
                      ? 'text-cricket-gold border-b-2 border-cricket-gold'
                      : 'text-white hover:text-cricket-gold'
                  }`}
                  style={{ fontSize: '13px', fontFamily: '"Work Sans", sans-serif' }}
                >
                  {item.label}
                </Link>

                {/* Dropdown Menu */}
                {item.children && activeDropdown === item.label && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    className="absolute top-full left-0 mt-1 w-48 bg-white rounded-md shadow-lg py-1 z-50"
                  >
                    {item.children.map((child) => (
                      <Link
                        key={child.href}
                        to={child.href}
                        className="block px-4 py-2 text-gray-700 hover:bg-cricket-light hover:text-cricket-green transition-colors duration-200"
                        style={{ fontSize: '13px', fontFamily: '"Work Sans", sans-serif' }}
                      >
                        {child.label}
                      </Link>
                    ))}
                  </motion.div>
                )}
              </div>
            ))}
          </nav>

          {/* Social Media & Search */}
          <div className="hidden md:flex items-center space-x-4">
            {/* Social Media Icons */}
            <div className="flex items-center space-x-2">
              <span className="text-white font-medium" style={{ fontSize: '13px', fontFamily: '"Work Sans", sans-serif' }}>Follow Us</span>
              <a href="#" className="text-white hover:text-cricket-gold transition-colors duration-200">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
              </a>
              <a href="#" className="text-white hover:text-cricket-gold transition-colors duration-200">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.174-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.099.12.112.225.085.345-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.402.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.357-.629-2.746-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24.009 12.017 24.009c6.624 0 11.99-5.367 11.99-11.988C24.007 5.367 18.641.001.012.001z"/>
                </svg>
              </a>
              <a href="#" className="text-white hover:text-cricket-gold transition-colors duration-200">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                </svg>
              </a>
            </div>

            {/* Fan Poll & Viewers Choice Icons */}
            <div className="flex items-center space-x-2">
              <button className="text-white hover:text-cricket-gold transition-colors duration-200" title="Fan Poll">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zM7 7v2h14V7H7z"/>
                </svg>
              </button>
              <button className="text-white hover:text-cricket-gold transition-colors duration-200" title="Viewers Choice">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </button>
            </div>

            {/* Search Icon */}
            <button className="text-white hover:text-cricket-gold transition-colors duration-200" title="Search">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={onMobileMenuToggle}
              className="inline-flex items-center justify-center p-2 rounded-md text-white hover:text-cricket-gold hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-cricket-gold"
              aria-expanded="false"
            >
              <span className="sr-only">Open main menu</span>
              <motion.div
                animate={{ rotate: isMobileMenuOpen ? 90 : 0 }}
                transition={{ duration: 0.2 }}
              >
                <svg
                  className="h-6 w-6"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  {isMobileMenuOpen ? (
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  ) : (
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 6h16M4 12h16M4 18h16"
                    />
                  )}
                </svg>
              </motion.div>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
