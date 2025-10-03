import React, { useState } from 'react'
import { Link, useLocation } from '@tanstack/react-router'
import { motion, AnimatePresence } from 'framer-motion'
import Header from './Header'
import Footer from './Footer'
import MobileMenu from './MobileMenu'

interface LayoutProps {
  children: React.ReactNode
}

function Layout({ children }: LayoutProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const location = useLocation()

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header 
        isMobileMenuOpen={isMobileMenuOpen}
        onMobileMenuToggle={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
      />
      
      <AnimatePresence>
        {isMobileMenuOpen && (
          <MobileMenu onClose={() => setIsMobileMenuOpen(false)} />
        )}
      </AnimatePresence>

      <main className="flex-1">
        <motion.div
          key={location.pathname}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          {children}
        </motion.div>
      </main>

      <Footer />
    </div>
  )
}

export default Layout
