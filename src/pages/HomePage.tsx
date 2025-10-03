import React from 'react'
import { motion } from 'framer-motion'
import HeroSection from '@/components/home/HeroSection'
import FeaturedVideos from '@/components/home/FeaturedVideos'
import TeamShowcase from '@/components/home/TeamShowcase'
import UpcomingMatches from '@/components/home/UpcomingMatches'
import PointsTable from '@/components/home/PointsTable'
import LatestNews from '@/components/home/LatestNews'
import PlayerSpotlight from '@/components/home/PlayerSpotlight'
import Statistics from '@/components/home/Statistics'

function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <HeroSection />

      {/* Featured Videos */}
      <FeaturedVideos />

      {/* Team Showcase */}
      <TeamShowcase />

      {/* Upcoming Matches */}
      <UpcomingMatches />

      {/* Points Table */}
      <PointsTable />

      {/* Latest News */}
      <LatestNews />

      {/* Player Spotlight */}
      <PlayerSpotlight />

      {/* Statistics */}
      <Statistics />
    </div>
  )
}

export default HomePage
