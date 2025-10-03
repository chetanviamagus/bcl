import React from 'react'
import { motion } from 'framer-motion'
import { Link } from '@tanstack/react-router'
import { mockTeams } from '@/data/mockData'

function PointsTable() {
  const sortedTeams = [...mockTeams].sort((a, b) => {
    if (a.stats.points !== b.stats.points) {
      return b.stats.points - a.stats.points
    }
    return b.stats.netRunRate - a.stats.netRunRate
  })

  return (
    <section className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Points Table
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Current standings in the Bellandur Cricket League
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          viewport={{ once: true }}
          className="bg-white rounded-xl shadow-lg overflow-hidden"
        >
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
                  <motion.tr
                    key={team.id}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.4, delay: index * 0.1 }}
                    viewport={{ once: true }}
                    className="hover:bg-gray-50/50 transition-colors duration-200"
                  >
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
                      <Link to="/teams/$teamId" params={{ teamId: team.id }} className="group">
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
                            <div className="text-sm font-medium text-gray-900 group-hover:text-primary-green transition-colors duration-200">
                              {team.name}
                            </div>
                            <div className="text-xs text-gray-500">
                              {team.captain}
                            </div>
                          </div>
                        </div>
                      </Link>
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
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="text-center mt-8"
        >
          <div className="flex flex-wrap justify-center gap-4 text-sm text-gray-600">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-gold rounded-full mr-2"></div>
              Top 3 Teams
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-primary-green-600 rounded-full mr-2"></div>
              Wins
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-red-600 rounded-full mr-2"></div>
              Losses
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          viewport={{ once: true }}
          className="text-center mt-8"
        >
          <Link
            to="/stats"
            className="btn btn-primary inline-flex items-center"
          >
            <span className="material-icons mr-2">bar_chart</span>
            View Detailed Stats
          </Link>
        </motion.div>
      </div>
    </section>
  )
}

export default PointsTable
