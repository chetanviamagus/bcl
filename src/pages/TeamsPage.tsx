import React from 'react'
import { motion } from 'framer-motion'
import { Link } from '@tanstack/react-router'
import { mockTeams } from '@/data/mockData'

function TeamsPage() {
  const sortedTeams = [...mockTeams].sort((a, b) => a.stats.position - b.stats.position)

  return (
    <div className="min-h-screen bg-cricket-light py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-cricket-dark mb-4">
            Our Teams
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Six competitive teams battling for the Bellandur Cricket League championship
          </p>
        </motion.div>

        {/* Teams Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {sortedTeams.map((team, index) => (
            <motion.div
              key={team.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ y: -5 }}
              className="group"
            >
              <Link to="/teams/$teamId" params={{ teamId: team.id }}>
                <div className="card card-hover h-full">
                  {/* Team Header */}
                  <div className="text-center mb-6">
                    <div 
                      className="w-24 h-24 mx-auto rounded-full flex items-center justify-center text-white text-2xl font-bold mb-4 shadow-lg"
                      style={{ backgroundColor: team.primaryColor }}
                    >
                      {team.shortName}
                    </div>
                    <h2 className="text-2xl font-bold text-cricket-dark group-hover:text-cricket-green transition-colors duration-200">
                      {team.name}
                    </h2>
                    <div className="text-sm text-gray-600">
                      Founded in {team.founded}
                    </div>
                  </div>

                  {/* Team Stats */}
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4 text-center">
                      <div className="bg-cricket-light rounded-lg p-3">
                        <div className="text-2xl font-bold text-cricket-green">
                          #{team.stats.position}
                        </div>
                        <div className="text-xs text-gray-600">Position</div>
                      </div>
                      <div className="bg-cricket-light rounded-lg p-3">
                        <div className="text-2xl font-bold text-cricket-green">
                          {team.stats.points}
                        </div>
                        <div className="text-xs text-gray-600">Points</div>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 text-center">
                      <div className="bg-cricket-light rounded-lg p-3">
                        <div className="text-lg font-bold text-cricket-dark">
                          {team.stats.matchesWon}
                        </div>
                        <div className="text-xs text-gray-600">Wins</div>
                      </div>
                      <div className="bg-cricket-light rounded-lg p-3">
                        <div className="text-lg font-bold text-cricket-dark">
                          {team.stats.matchesLost}
                        </div>
                        <div className="text-xs text-gray-600">Losses</div>
                      </div>
                    </div>
                  </div>

                  {/* Team Details */}
                  <div className="mt-6 pt-4 border-t border-gray-200 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Captain:</span>
                      <span className="font-medium text-cricket-dark">{team.captain}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Coach:</span>
                      <span className="font-medium text-cricket-dark">{team.coach}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Home Ground:</span>
                      <span className="font-medium text-cricket-dark text-sm">{team.homeGround}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Net Run Rate:</span>
                      <span className={`font-mono text-sm ${
                        team.stats.netRunRate >= 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {team.stats.netRunRate > 0 ? '+' : ''}{team.stats.netRunRate.toFixed(3)}
                      </span>
                    </div>
                  </div>

                  {/* Hover Effect */}
                  <div className="absolute inset-0 bg-cricket-green/5 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
                </div>
              </Link>
            </motion.div>
          ))}
        </div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="text-center mt-16"
        >
          <div className="bg-white rounded-xl p-8 shadow-lg">
            <h3 className="text-2xl font-bold text-cricket-dark mb-4">
              Want to know more about our teams?
            </h3>
            <p className="text-gray-600 mb-6">
              Click on any team to view detailed information, player rosters, and match history.
            </p>
            <Link
              to="/stats"
              className="btn btn-primary inline-flex items-center"
            >
              <span className="material-icons mr-2">bar_chart</span>
              View Team Statistics
            </Link>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default TeamsPage
