import React from 'react'
import { motion } from 'framer-motion'

function AboutPage() {
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
            About BCL
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Learn more about Bellandur Cricket League and our mission
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mb-16">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h2 className="text-3xl font-bold text-cricket-dark mb-6">Our Story</h2>
            <p className="text-gray-600 mb-4">
              Bellandur Cricket League (BCL) was established to promote cricket at the grassroots level 
              in the Bellandur area. We believe in fostering talent, building community, and creating 
              opportunities for cricket enthusiasts to showcase their skills.
            </p>
            <p className="text-gray-600 mb-4">
              Our league features six competitive teams that battle it out throughout the season, 
              providing exciting cricket action for fans and players alike. We are committed to 
              maintaining the highest standards of sportsmanship and fair play.
            </p>
            <p className="text-gray-600">
              Join us in celebrating the spirit of cricket and supporting local talent in their 
              journey to excellence.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="bg-white rounded-xl shadow-lg p-8"
          >
            <h3 className="text-2xl font-bold text-cricket-dark mb-6">Quick Facts</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Founded:</span>
                <span className="font-medium text-cricket-dark">2020</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Teams:</span>
                <span className="font-medium text-cricket-dark">6</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Matches per Season:</span>
                <span className="font-medium text-cricket-dark">30</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Format:</span>
                <span className="font-medium text-cricket-dark">T20</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Venues:</span>
                <span className="font-medium text-cricket-dark">6</span>
              </div>
            </div>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="bg-white rounded-xl shadow-lg p-8"
        >
          <h2 className="text-3xl font-bold text-cricket-dark mb-6 text-center">Our Mission</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-cricket-green rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="material-icons text-white text-2xl">sports_cricket</span>
              </div>
              <h3 className="text-xl font-bold text-cricket-dark mb-2">Promote Cricket</h3>
              <p className="text-gray-600">
                Encourage cricket participation at all levels and nurture local talent.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-cricket-gold rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="material-icons text-cricket-dark text-2xl">groups</span>
              </div>
              <h3 className="text-xl font-bold text-cricket-dark mb-2">Build Community</h3>
              <p className="text-gray-600">
                Create a strong cricket community that brings people together through sport.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="material-icons text-white text-2xl">emoji_events</span>
              </div>
              <h3 className="text-xl font-bold text-cricket-dark mb-2">Excellence</h3>
              <p className="text-gray-600">
                Maintain high standards of play and sportsmanship in all our activities.
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default AboutPage
