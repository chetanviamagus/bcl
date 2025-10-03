import React from 'react'
import { motion } from 'framer-motion'
import { Link } from '@tanstack/react-router'
import { mockPlayers } from '@/data/mockData'

function PlayerSpotlight() {
  const featuredPlayers = mockPlayers.slice(0, 3)

  return (
    <section className="py-16 bg-cricket-light">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-cricket-dark mb-4">
            Player Spotlight
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Meet the stars of Bellandur Cricket League
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {featuredPlayers.map((player, index) => (
            <motion.div
              key={player.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="group"
            >
              <div className="card card-hover h-full">
                {/* Player Photo */}
                <div className="text-center mb-6">
                  <div className="w-24 h-24 mx-auto bg-gradient-to-br from-cricket-green to-green-800 rounded-full flex items-center justify-center mb-4">
                    <span className="material-icons text-white text-3xl">person</span>
                  </div>
                  <h3 className="text-xl font-bold text-cricket-dark group-hover:text-cricket-green transition-colors duration-200">
                    {player.name}
                  </h3>
                  <div className="text-sm text-gray-600">
                    #{player.jerseyNumber} • {player.role}
                  </div>
                </div>

                {/* Player Stats */}
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-4 text-center">
                    <div className="bg-cricket-light rounded-lg p-3">
                      <div className="text-2xl font-bold text-cricket-green">
                        {player.stats.runs}
                      </div>
                      <div className="text-xs text-gray-600">Runs</div>
                    </div>
                    <div className="bg-cricket-light rounded-lg p-3">
                      <div className="text-2xl font-bold text-cricket-green">
                        {player.stats.wickets}
                      </div>
                      <div className="text-xs text-gray-600">Wickets</div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-center">
                    <div className="bg-cricket-light rounded-lg p-3">
                      <div className="text-lg font-bold text-cricket-dark">
                        {player.stats.average}
                      </div>
                      <div className="text-xs text-gray-600">Average</div>
                    </div>
                    <div className="bg-cricket-light rounded-lg p-3">
                      <div className="text-lg font-bold text-cricket-dark">
                        {player.stats.strikeRate}
                      </div>
                      <div className="text-xs text-gray-600">Strike Rate</div>
                    </div>
                  </div>
                </div>

                {/* Player Details */}
                <div className="mt-6 pt-4 border-t border-gray-200">
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Age:</span>
                      <span className="font-medium text-cricket-dark">{player.age}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Nationality:</span>
                      <span className="font-medium text-cricket-dark">{player.nationality}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Batting:</span>
                      <span className="font-medium text-cricket-dark">{player.battingStyle}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Bowling:</span>
                      <span className="font-medium text-cricket-dark">{player.bowlingStyle}</span>
                    </div>
                  </div>
                </div>

                {/* Hover Effect */}
                <div className="absolute inset-0 bg-cricket-green/5 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
              </div>
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
            to="/stats"
            className="btn btn-primary inline-flex items-center"
          >
            <span className="material-icons mr-2">emoji_events</span>
            View All Players
          </Link>
        </motion.div>
      </div>
    </section>
  )
}

export default PlayerSpotlight
