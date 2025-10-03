import React from 'react'
import { useParams } from '@tanstack/react-router'
import { motion } from 'framer-motion'
import { getTeamById, getPlayersByTeamId } from '@/data/mockData'

function TeamDetailPage() {
  const { teamId } = useParams({ from: '/teams/$teamId' })
  const team = getTeamById(teamId)
  const players = getPlayersByTeamId(teamId)

  if (!team) {
    return (
      <div className="min-h-screen bg-cricket-light flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-cricket-dark mb-4">Team Not Found</h1>
          <p className="text-gray-600">The team you're looking for doesn't exist.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-cricket-light py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Team Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <div 
            className="w-32 h-32 mx-auto rounded-full flex items-center justify-center text-white text-4xl font-bold mb-6 shadow-lg"
            style={{ backgroundColor: team.primaryColor }}
          >
            {team.shortName}
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-cricket-dark mb-4">
            {team.name}
          </h1>
          <p className="text-xl text-gray-600">
            Founded in {team.founded} • {team.homeGround}
          </p>
        </motion.div>

        {/* Team Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="bg-white rounded-xl shadow-lg p-8 mb-12"
        >
          <h2 className="text-2xl font-bold text-cricket-dark mb-6 text-center">Team Statistics</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-cricket-green">#{team.stats.position}</div>
              <div className="text-gray-600">Position</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-cricket-green">{team.stats.points}</div>
              <div className="text-gray-600">Points</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-cricket-dark">{team.stats.matchesWon}</div>
              <div className="text-gray-600">Wins</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-cricket-dark">{team.stats.matchesLost}</div>
              <div className="text-gray-600">Losses</div>
            </div>
          </div>
        </motion.div>

        {/* Players */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="bg-white rounded-xl shadow-lg p-8"
        >
          <h2 className="text-2xl font-bold text-cricket-dark mb-6 text-center">Squad</h2>
          {players.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {players.map((player, index) => (
                <motion.div
                  key={player.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  className="bg-cricket-light rounded-lg p-4"
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-cricket-green rounded-full flex items-center justify-center">
                      <span className="text-white font-bold">#{player.jerseyNumber}</span>
                    </div>
                    <div>
                      <h3 className="font-bold text-cricket-dark">{player.name}</h3>
                      <p className="text-sm text-gray-600">{player.role}</p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-600">
              <span className="material-icons text-4xl mb-4 block">person</span>
              <p>No players found for this team.</p>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}

export default TeamDetailPage
