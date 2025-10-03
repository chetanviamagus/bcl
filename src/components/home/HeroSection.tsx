import React from 'react'
import { motion } from 'framer-motion'
import { Link } from '@tanstack/react-router'

function HeroSection() {
  return (
    <section className="relative bg-gradient-to-r from-cricket-green to-green-800 text-white overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0 bg-[url('/images/cricket-pattern.svg')] bg-repeat"></div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Content */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="space-y-8"
          >
            <div className="space-y-4">
              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2, duration: 0.8 }}
                className="text-4xl md:text-6xl font-bold leading-tight"
              >
                Bellandur
                <span className="block text-cricket-gold">Cricket League</span>
              </motion.h1>
              
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4, duration: 0.8 }}
                className="text-xl md:text-2xl text-gray-200"
              >
                Premier Cricket League featuring 6 competitive teams
              </motion.p>
            </div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6, duration: 0.8 }}
              className="space-y-4"
            >
              <p className="text-lg text-gray-300 max-w-2xl">
                Experience the thrill of cricket with our exciting league featuring 
                the best teams from Bellandur. Watch live matches, track statistics, 
                and join the fantasy league.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4">
                <Link
                  to="/matches"
                  className="btn btn-secondary text-lg px-8 py-4 inline-flex items-center justify-center"
                >
                  <span className="material-icons mr-2">sports_cricket</span>
                  View Matches
                </Link>
                
                <Link
                  to="/teams"
                  className="btn btn-outline border-white text-white hover:bg-white hover:text-cricket-green text-lg px-8 py-4 inline-flex items-center justify-center"
                >
                  <span className="material-icons mr-2">groups</span>
                  Explore Teams
                </Link>
              </div>
            </motion.div>

            {/* Quick Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8, duration: 0.8 }}
              className="grid grid-cols-3 gap-6 pt-8"
            >
              <div className="text-center">
                <div className="text-3xl font-bold text-cricket-gold">6</div>
                <div className="text-sm text-gray-300">Teams</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-cricket-gold">30</div>
                <div className="text-sm text-gray-300">Matches</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-cricket-gold">2024</div>
                <div className="text-sm text-gray-300">Season</div>
              </div>
            </motion.div>
          </motion.div>

          {/* Hero Image/Video */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4, duration: 0.8 }}
            className="relative"
          >
            <div className="relative bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
              {/* Placeholder for hero image/video */}
              <div className="aspect-video bg-gradient-to-br from-cricket-gold/20 to-cricket-green/20 rounded-xl flex items-center justify-center">
                <div className="text-center">
                  <motion.div
                    animate={{ 
                      scale: [1, 1.1, 1],
                      rotate: [0, 5, -5, 0]
                    }}
                    transition={{ 
                      duration: 2,
                      repeat: Infinity,
                      ease: "easeInOut"
                    }}
                    className="w-24 h-24 bg-cricket-gold rounded-full flex items-center justify-center mx-auto mb-4"
                  >
                    <span className="material-icons text-4xl text-cricket-dark">sports_cricket</span>
                  </motion.div>
                  <h3 className="text-2xl font-bold text-white mb-2">Live Action</h3>
                  <p className="text-gray-300">Watch thrilling cricket matches</p>
                </div>
              </div>
              
              {/* Floating elements */}
              <motion.div
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                className="absolute -top-4 -right-4 w-8 h-8 bg-cricket-gold rounded-full flex items-center justify-center"
              >
                <span className="material-icons text-cricket-dark text-sm">star</span>
              </motion.div>
              
              <motion.div
                animate={{ y: [0, 10, 0] }}
                transition={{ duration: 2, repeat: Infinity, ease: "easeInOut", delay: 1 }}
                className="absolute -bottom-4 -left-4 w-6 h-6 bg-white/20 rounded-full flex items-center justify-center"
              >
                <span className="material-icons text-white text-xs">favorite</span>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Bottom Wave */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg
          className="w-full h-16 text-white"
          viewBox="0 0 1200 120"
          preserveAspectRatio="none"
        >
          <path
            d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z"
            opacity=".25"
            fill="currentColor"
          />
          <path
            d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z"
            opacity=".5"
            fill="currentColor"
          />
          <path
            d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z"
            fill="currentColor"
          />
        </svg>
      </div>
    </section>
  )
}

export default HeroSection
