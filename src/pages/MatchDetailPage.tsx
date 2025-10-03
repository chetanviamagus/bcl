import React from 'react'
import { useParams } from '@tanstack/react-router'
import { motion } from 'framer-motion'

function MatchDetailPage() {
  const { matchId } = useParams({ from: '/matches/$matchId' })

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
            Match Details
          </h1>
          <p className="text-xl text-gray-600">
            Match ID: {matchId}
          </p>
          <div className="mt-8 bg-white rounded-xl shadow-lg p-8">
            <p className="text-gray-600">Match details will be implemented here.</p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default MatchDetailPage
