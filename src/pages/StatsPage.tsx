import React from 'react'
import { motion } from 'framer-motion'
import { mockTeams, mockPlayers } from '@/data/mockData'

function StatsPage() {
  const sortedTeams = [...mockTeams].sort((a, b) => b.stats.points - a.stats.points)
  const topRunScorers = [...mockPlayers].sort((a, b) => b.stats.runs - a.stats.runs).slice(0, 5)
  const topWicketTakers = [...mockPlayers].sort((a, b) => b.stats.wickets - a.stats.wickets).slice(0, 5)

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Statistics
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Comprehensive statistics and performance metrics for Bellandur Cricket League
          </p>
        </motion.div>

        {/* Points Table */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="bg-white rounded-xl shadow-lg p-8 mb-12"
        >
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">Points Table</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-primary-green text-white">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-medium">#</th>
                  <th className="px-6 py-4 text-left text-sm font-medium">Team</th>
                  <th className="px-6 py-4 text-center text-sm font-medium">P</th>
                  <th className="px-6 py-4 text-center text-sm font-medium">W</th>
                  <th className="px-6 py-4 text-center text-sm font-medium">L</th>
                  <th className="px-6 py-4 text-center text-sm font-medium">Pts</th>
                  <th className="px-6 py-4 text-center text-sm font-medium">NRR</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {sortedTeams.map((team, index) => (
                  <tr key={team.id} className="hover:bg-gray-50/50 transition-colors duration-200">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <span className={`text-lg font-bold ${
                          index < 3 ? 'text-gold' : 'text-gray-600'
                        }`}>
                          {index + 1}
                        </span>
                        {index < 3 && (
                          <span className="ml-2 material-icons text-gold text-sm">
                            emoji_events
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 rounded-full flex items-center justify-center overflow-hidden">
                          <img
                            src={team.logo}
                            alt={team.name}
                            className="w-full h-full object-cover"
                            onError={(e) => {
                              const target = e.target as HTMLImageElement
                              target.style.display = 'none'
                              target.nextElementSibling?.classList.remove('hidden')
                            }}
                          />
                          <div 
                            className="w-full h-full flex items-center justify-center text-white text-sm font-bold hidden"
                            style={{ backgroundColor: team.primaryColor }}
                          >
                            {team.shortName}
                          </div>
                        </div>
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {team.name}
                          </div>
                          <div className="text-xs text-gray-500">
                            {team.captain}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      {team.stats.matchesPlayed}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-primary-green-600 font-medium">
                      {team.stats.matchesWon}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-red-600 font-medium">
                      {team.stats.matchesLost}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm font-bold text-gray-900">
                      {team.stats.points}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      <span className={`font-mono ${
                        team.stats.netRunRate >= 0 ? 'text-primary-green-600' : 'text-red-600'
                      }`}>
                        {team.stats.netRunRate > 0 ? '+' : ''}{team.stats.netRunRate.toFixed(3)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Top Run Scorers */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="bg-white rounded-xl shadow-lg p-8"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">Top Run Scorers</h2>
            <div className="space-y-4">
              {topRunScorers.map((player, index) => (
                <div key={player.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-primary-green rounded-full flex items-center justify-center text-white font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <div className="font-medium text-gray-900">{player.name}</div>
                      <div className="text-sm text-gray-600">{player.role}</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-primary-green">{player.stats.runs}</div>
                    <div className="text-xs text-gray-600">runs</div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Top Wicket Takers */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
            className="bg-white rounded-xl shadow-lg p-8"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">Top Wicket Takers</h2>
            <div className="space-y-4">
              {topWicketTakers.map((player, index) => (
                <div key={player.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-gold rounded-full flex items-center justify-center text-gray-900 font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <div className="font-medium text-gray-900">{player.name}</div>
                      <div className="text-sm text-gray-600">{player.role}</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-gold">{player.stats.wickets}</div>
                    <div className="text-xs text-gray-600">wickets</div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default StatsPage
