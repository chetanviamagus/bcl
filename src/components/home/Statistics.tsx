import React from 'react'
import { motion } from 'framer-motion'
import { mockTeams, mockPlayers } from '@/data/mockData'

function Statistics() {
  const totalRuns = mockPlayers.reduce((sum, player) => sum + player.stats.runs, 0)
  const totalWickets = mockPlayers.reduce((sum, player) => sum + player.stats.wickets, 0)
  const totalMatches = mockTeams.reduce((sum, team) => sum + team.stats.matchesPlayed, 0) / 2 // Divide by 2 since each match involves 2 teams
  const totalPlayers = mockPlayers.length

  const stats = [
    {
      title: 'Total Runs',
      value: totalRuns.toLocaleString(),
      icon: 'sports_cricket',
      color: 'text-cricket-green',
      bgColor: 'bg-cricket-green/10'
    },
    {
      title: 'Total Wickets',
      value: totalWickets.toLocaleString(),
      icon: 'sports_handball',
      color: 'text-cricket-gold',
      bgColor: 'bg-cricket-gold/10'
    },
    {
      title: 'Matches Played',
      value: totalMatches.toString(),
      icon: 'sports',
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      title: 'Total Players',
      value: totalPlayers.toString(),
      icon: 'groups',
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    }
  ]

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
          <h2 className="text-3xl md:text-4xl font-bold text-cricket-dark mb-4">
            League Statistics
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Numbers that tell the story of our cricket league
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              whileHover={{ scale: 1.05 }}
              className="group"
            >
              <div className="card text-center h-full">
                <div className={`w-16 h-16 mx-auto mb-4 rounded-full ${stat.bgColor} flex items-center justify-center group-hover:scale-110 transition-transform duration-300`}>
                  <span className={`material-icons text-2xl ${stat.color}`}>
                    {stat.icon}
                  </span>
                </div>
                
                <div className="space-y-2">
                  <div className={`text-3xl font-bold ${stat.color} scoreboard`}>
                    {stat.value}
                  </div>
                  <div className="text-gray-600 font-medium">
                    {stat.title}
                  </div>
                </div>

                {/* Animated background */}
                <div className={`absolute inset-0 rounded-xl ${stat.bgColor} opacity-0 group-hover:opacity-20 transition-opacity duration-300 pointer-events-none`} />
              </div>
            </motion.div>
          ))}
        </div>

        {/* Additional Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="mt-16"
        >
          <div className="bg-cricket-light rounded-xl p-8">
            <h3 className="text-2xl font-bold text-cricket-dark text-center mb-8">
              Season Highlights
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="text-4xl font-bold text-cricket-green mb-2">
                  {Math.max(...mockTeams.map(team => team.stats.points))}
                </div>
                <div className="text-gray-600">Highest Points</div>
                <div className="text-sm text-cricket-dark font-medium">
                  {mockTeams.find(team => team.stats.points === Math.max(...mockTeams.map(t => t.stats.points)))?.name}
                </div>
              </div>
              
              <div className="text-center">
                <div className="text-4xl font-bold text-cricket-gold mb-2">
                  {Math.max(...mockPlayers.map(player => player.stats.runs))}
                </div>
                <div className="text-gray-600">Most Runs</div>
                <div className="text-sm text-cricket-dark font-medium">
                  {mockPlayers.find(player => player.stats.runs === Math.max(...mockPlayers.map(p => p.stats.runs)))?.name}
                </div>
              </div>
              
              <div className="text-center">
                <div className="text-4xl font-bold text-blue-600 mb-2">
                  {Math.max(...mockPlayers.map(player => player.stats.wickets))}
                </div>
                <div className="text-gray-600">Most Wickets</div>
                <div className="text-sm text-cricket-dark font-medium">
                  {mockPlayers.find(player => player.stats.wickets === Math.max(...mockPlayers.map(p => p.stats.wickets)))?.name}
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}

export default Statistics
