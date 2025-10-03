import React from 'react'
import { motion } from 'framer-motion'

function FantasyPage() {
  return (
    <div className="min-h-screen bg-cricket-light py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-cricket-dark mb-4">
            Fantasy League
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Create your dream team and compete with other cricket fans
          </p>
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="text-center">
              <span className="material-icons text-6xl text-cricket-green mb-4 block">sports_cricket</span>
              <h2 className="text-2xl font-bold text-cricket-dark mb-4">Coming Soon</h2>
              <p className="text-gray-600 mb-6">
                Fantasy league features will be available soon. Stay tuned for updates!
              </p>
              <div className="bg-cricket-light rounded-lg p-4">
                <p className="text-sm text-gray-600">
                  Create your team, select players, and compete for prizes in our upcoming fantasy cricket league.
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default FantasyPage
