import React from 'react'
import { motion } from 'framer-motion'
import { Link } from '@tanstack/react-router'
import { getUpcomingMatches } from '@/data/mockData'

function UpcomingMatches() {
  const upcomingMatches = getUpcomingMatches().slice(0, 3)

  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Upcoming Matches
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Don't miss the exciting cricket action coming up
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {upcomingMatches.map((match, index) => (
            <motion.div
              key={match.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="group"
            >
              <Link to="/matches/$matchId" params={{ matchId: match.id }}>
                <div className="card card-hover h-full">
                  {/* Match Header */}
                  <div className="text-center mb-6">
                    <div className="text-sm text-primary-green font-medium mb-2">
                      {new Date(match.date).toLocaleDateString('en-US', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}
                    </div>
                    <div className="text-lg font-bold text-gray-900">
                      {match.time}
                    </div>
                  </div>

                  {/* Teams */}
                  <div className="space-y-4 mb-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-primary-green rounded-full flex items-center justify-center">
                          <span className="text-white text-sm font-bold">
                            {match.homeTeam.split(' ').map(word => word[0]).join('')}
                          </span>
                        </div>
                        <span className="font-medium text-gray-900">
                          {match.homeTeam}
                        </span>
                      </div>
                    </div>

                    <div className="text-center text-gray-500 font-medium">
                      VS
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-gold rounded-full flex items-center justify-center">
                          <span className="text-gray-900 text-sm font-bold">
                            {match.awayTeam.split(' ').map(word => word[0]).join('')}
                          </span>
                        </div>
                        <span className="font-medium text-gray-900">
                          {match.awayTeam}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Venue */}
                  <div className="text-center text-sm text-gray-600 mb-4">
                    <span className="material-icons text-base mr-1">location_on</span>
                    {match.venue}
                  </div>

                  {/* Toss Info */}
                  {match.tossWinner && (
                    <div className="text-center text-xs text-gray-500 bg-gray-50 rounded-lg p-2">
                      Toss: {match.tossWinner} chose to {match.tossDecision}
                    </div>
                  )}

                  {/* Hover Effect */}
                  <div className="absolute inset-0 bg-primary-green/5 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
                </div>
              </Link>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="text-center mt-12"
        >
          <Link
            to="/matches"
            className="btn btn-primary inline-flex items-center"
          >
            <span className="material-icons mr-2">sports_cricket</span>
            View All Matches
          </Link>
        </motion.div>
      </div>
    </section>
  )
}

export default UpcomingMatches
