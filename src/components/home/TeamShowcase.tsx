import React from 'react'
import { motion } from 'framer-motion'
import { Link } from '@tanstack/react-router'
import { mockTeams } from '@/data/mockData'

function TeamShowcase() {
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
            Our Teams
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Six competitive teams battling for the championship
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {mockTeams.map((team, index) => (
            <motion.div
              key={team.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              whileHover={{ y: -5 }}
              className="group"
            >
              <Link to="/teams/$teamId" params={{ teamId: team.id }}>
                <div className="card card-hover h-full">
                  {/* Team Logo */}
                  <div className="text-center mb-6">
                    <div className="w-20 h-20 mx-auto rounded-full flex items-center justify-center mb-4 overflow-hidden">
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
                        className="w-full h-full flex items-center justify-center text-white text-2xl font-bold hidden"
                        style={{ backgroundColor: team.primaryColor }}
                      >
                        {team.shortName}
                      </div>
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 group-hover:text-primary-green transition-colors duration-200">
                      {team.name}
                    </h3>
                  </div>

                  {/* Team Stats */}
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Captain:</span>
                      <span className="font-medium text-gray-900">{team.captain}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Coach:</span>
                      <span className="font-medium text-gray-900">{team.coach}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Founded:</span>
                      <span className="font-medium text-gray-900">{team.founded}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Home Ground:</span>
                      <span className="font-medium text-gray-900 text-sm">{team.homeGround}</span>
                    </div>
                  </div>

                  {/* Position Badge */}
                  <div className="mt-6 pt-4 border-t border-gray-200">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Current Position:</span>
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl font-bold text-primary-green">
                          #{team.stats.position}
                        </span>
                        <div className="text-right">
                          <div className="text-sm font-medium text-gray-900">
                            {team.stats.points} pts
                          </div>
                          <div className="text-xs text-gray-500">
                            {team.stats.matchesWon}W-{team.stats.matchesLost}L
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

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
          transition={{ duration: 0.6, delay: 0.6 }}
          viewport={{ once: true }}
          className="text-center mt-12"
        >
          <Link
            to="/teams"
            className="btn btn-primary inline-flex items-center"
          >
            <span className="material-icons mr-2">groups</span>
            View All Teams
          </Link>
        </motion.div>
      </div>
    </section>
  )
}

export default TeamShowcase
