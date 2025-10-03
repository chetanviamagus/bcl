import React from 'react'
import { motion } from 'framer-motion'
import { mockVideos } from '@/data/mockData'

function VideosPage() {
  return (
    <div className="min-h-screen bg-cricket-light py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-cricket-dark mb-4">
            Videos
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Watch highlights, interviews, and exclusive content from Bellandur Cricket League
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {mockVideos.map((video, index) => (
            <motion.div
              key={video.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="group"
            >
              <div className="relative bg-gray-900 rounded-xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
                <div className="aspect-video bg-gradient-to-br from-cricket-green to-green-800 relative overflow-hidden">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <motion.div
                      whileHover={{ scale: 1.1 }}
                      className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center cursor-pointer"
                    >
                      <span className="material-icons text-white text-2xl ml-1">play_arrow</span>
                    </motion.div>
                  </div>
                  
                  <div className="absolute bottom-4 right-4 bg-black/70 text-white px-2 py-1 rounded text-sm">
                    {video.duration}
                  </div>
                  
                  <div className="absolute top-4 right-4 bg-cricket-gold text-cricket-dark px-2 py-1 rounded text-sm font-medium">
                    {video.views.toLocaleString()} views
                  </div>
                </div>

                <div className="p-6">
                  <h3 className="text-lg font-semibold text-white mb-2 group-hover:text-cricket-gold transition-colors duration-200">
                    {video.title}
                  </h3>
                  <p className="text-gray-300 text-sm mb-4">
                    {video.description}
                  </p>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-400 uppercase tracking-wide">
                      {video.category}
                    </span>
                    <span className="text-xs text-gray-400">
                      {new Date(video.publishedAt).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default VideosPage
