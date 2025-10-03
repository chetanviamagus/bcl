import React from 'react'
import { motion } from 'framer-motion'
import { Link } from '@tanstack/react-router'
import { mockMatches } from '@/data/mockData'

function MatchesPage() {
  const upcomingMatches = mockMatches.filter(match => match.status === 'upcoming')
  const completedMatches = mockMatches.filter(match => match.status === 'completed')
  const liveMatches = mockMatches.filter(match => match.status === 'live')

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Matches
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Follow all the exciting cricket action in Bellandur Cricket League
          </p>
        </motion.div>

        {/* Live Matches */}
        {liveMatches.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mb-12"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <span className="w-3 h-3 bg-red-500 rounded-full mr-3 animate-pulse"></span>
              Live Matches
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {liveMatches.map((match, index) => (
                <motion.div
                  key={match.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  className="group"
                >
                  <Link to="/matches/$matchId" params={{ matchId: match.id }}>
                    <div className="card card-hover h-full border-2 border-red-500">
                      <div className="text-center mb-4">
                        <div className="text-sm text-red-600 font-medium mb-2 flex items-center justify-center">
                          <span className="w-2 h-2 bg-red-500 rounded-full mr-2 animate-pulse"></span>
                          LIVE
                        </div>
                        <div className="text-lg font-bold text-gray-900">
                          {match.homeTeam} vs {match.awayTeam}
                        </div>
                        <div className="text-sm text-gray-600">{match.venue}</div>
                      </div>
                      {match.score && (
                        <div className="text-center">
                          <div className="text-2xl font-bold text-primary-green">
                            {match.score.homeTeam.runs}/{match.score.homeTeam.wickets}
                          </div>
                          <div className="text-sm text-gray-600">
                            {match.score.homeTeam.overs} overs
                          </div>
                        </div>
                      )}
                    </div>
                  </Link>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Upcoming Matches */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mb-12"
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Upcoming Matches</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {upcomingMatches.map((match, index) => (
              <motion.div
                key={match.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                className="group"
              >
                <Link to="/matches/$matchId" params={{ matchId: match.id }}>
                  <div className="card card-hover h-full">
                    <div className="text-center mb-4">
                      <div className="text-sm text-primary-green font-medium mb-2">
                        {new Date(match.date).toLocaleDateString('en-US', {
                          weekday: 'long',
                          month: 'short',
                          day: 'numeric'
                        })}
                      </div>
                      <div className="text-lg font-bold text-gray-900">
                        {match.homeTeam} vs {match.awayTeam}
                      </div>
                      <div className="text-sm text-gray-600">{match.venue}</div>
                      <div className="text-sm text-gray-600">{match.time}</div>
                    </div>
                    {match.tossWinner && (
                      <div className="text-center text-xs text-gray-500 bg-gray-50 rounded-lg p-2">
                        Toss: {match.tossWinner} chose to {match.tossDecision}
                      </div>
                    )}
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Completed Matches */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Results</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {completedMatches.map((match, index) => (
              <motion.div
                key={match.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                className="group"
              >
                <Link to="/matches/$matchId" params={{ matchId: match.id }}>
                  <div className="card card-hover h-full">
                    <div className="text-center mb-4">
                      <div className="text-sm text-gray-500 font-medium mb-2">
                        {new Date(match.date).toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric'
                        })}
                      </div>
                      <div className="text-lg font-bold text-gray-900">
                        {match.homeTeam} vs {match.awayTeam}
                      </div>
                      <div className="text-sm text-gray-600">{match.venue}</div>
                    </div>
                    {match.score && (
                      <div className="text-center">
                        <div className="text-lg font-bold text-primary-green mb-2">
                          {match.result}
                        </div>
                        <div className="text-sm text-gray-600">
                          {match.score.homeTeam.runs}/{match.score.homeTeam.wickets} vs {match.score.awayTeam.runs}/{match.score.awayTeam.wickets}
                        </div>
                      </div>
                    )}
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default MatchesPage
