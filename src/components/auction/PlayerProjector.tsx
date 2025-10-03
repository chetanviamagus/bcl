import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { AuctionPlayer } from '@/types'
import { mockTeams } from '@/data/mockData'

interface PlayerProjectorProps {
  players: AuctionPlayer[]
  currentPlayerIndex: number
  onPlayerChange: (index: number) => void
  onBid: (playerId: string, teamId: string, amount: number) => void
  teamBudgets: any[]
  onBackToList?: () => void
}

function PlayerProjector({ 
  players, 
  currentPlayerIndex, 
  onPlayerChange, 
  onBid, 
  teamBudgets,
  onBackToList
}: PlayerProjectorProps) {
  const [bidAmount, setBidAmount] = useState<number>(0)
  const [selectedTeam, setSelectedTeam] = useState<string>('')
  const [isBidding, setIsBidding] = useState<boolean>(false)

  const currentPlayer = players[currentPlayerIndex]

  useEffect(() => {
    setBidAmount(currentPlayer?.basePrice || 0)
    setSelectedTeam('')
    setIsBidding(false)
  }, [currentPlayer])

  // Keyboard navigation
  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      if (event.key === 'ArrowLeft' && currentPlayerIndex > 0) {
        handlePrevious()
      } else if (event.key === 'ArrowRight' && currentPlayerIndex < players.length - 1) {
        handleNext()
      } else if (event.key === 'Escape') {
        setIsBidding(false)
      }
    }

    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [currentPlayerIndex, players.length])

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount)
  }

  const getRoleColor = (role: string) => {
    const colors = {
      'Batsman': 'bg-green-500',
      'Bowler': 'bg-red-500',
      'All-rounder': 'bg-blue-500',
      'Wicket-keeper': 'bg-purple-500'
    }
    return colors[role as keyof typeof colors] || 'bg-gray-500'
  }

  const getStatusColor = (status: string) => {
    const colors = {
      'available': 'bg-yellow-500',
      'sold': 'bg-green-500',
      'unsold': 'bg-red-500'
    }
    return colors[status as keyof typeof colors] || 'bg-gray-500'
  }

  const handleBid = () => {
    if (selectedTeam && bidAmount > currentPlayer.currentBid) {
      onBid(currentPlayer.id, selectedTeam, bidAmount)
      setIsBidding(false)
    }
  }

  const handleNext = () => {
    if (currentPlayerIndex < players.length - 1) {
      onPlayerChange(currentPlayerIndex + 1)
    }
  }

  const handlePrevious = () => {
    if (currentPlayerIndex > 0) {
      onPlayerChange(currentPlayerIndex - 1)
    }
  }

  if (!currentPlayer) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-2xl">No players available</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Projector Header */}
      <div className="bg-black py-4 px-8 border-b border-gray-700">
        <div className="flex justify-between items-center">
          <div className="text-2xl font-bold">BCL 2024 Player Auction</div>
          <div className="flex items-center space-x-4">
            <div className="text-lg">
              Player {currentPlayerIndex + 1} of {players.length}
            </div>
            {onBackToList && (
              <button
                onClick={onBackToList}
                className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200"
              >
                Back to List
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Main Projector Display */}
      <div className="flex h-screen">
        {/* Player Information Panel */}
        <div className="flex-1 p-8">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentPlayer.id}
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -50 }}
              transition={{ duration: 0.5 }}
              className="h-full flex flex-col"
            >
              {/* Player Header */}
              <div className="flex items-start space-x-8 mb-8">
                {/* Player Photo/Initials */}
                <div className="w-32 h-32 bg-gray-700 rounded-full flex items-center justify-center">
                  {currentPlayer.photo ? (
                    <img 
                      src={currentPlayer.photo} 
                      alt={currentPlayer.name}
                      className="w-full h-full rounded-full object-cover"
                    />
                  ) : (
                    <span className="text-4xl font-bold text-gray-300">
                      {currentPlayer.name.split(' ').map(n => n[0]).join('')}
                    </span>
                  )}
                </div>

                {/* Player Basic Info */}
                <div className="flex-1">
                  <div className="flex items-center space-x-4 mb-4">
                    <h1 className="text-5xl font-bold">{currentPlayer.name}</h1>
                    <div className={`px-4 py-2 rounded-full text-lg font-semibold ${getStatusColor(currentPlayer.status)}`}>
                      {currentPlayer.status.toUpperCase()}
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-6 text-2xl">
                    <div className={`px-4 py-2 rounded-lg ${getRoleColor(currentPlayer.role)}`}>
                      {currentPlayer.role}
                    </div>
                    <span>Age: {currentPlayer.age}</span>
                    <span>{currentPlayer.nationality}</span>
                  </div>
                </div>
              </div>

              {/* Player Stats Grid */}
              <div className="grid grid-cols-2 gap-8 mb-8">
                <div className="bg-gray-800 rounded-lg p-6">
                  <h3 className="text-2xl font-semibold mb-4 text-gray-300">Batting Stats</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between text-xl">
                      <span>Matches:</span>
                      <span className="font-semibold">{currentPlayer.stats.matches}</span>
                    </div>
                    <div className="flex justify-between text-xl">
                      <span>Runs:</span>
                      <span className="font-semibold">{currentPlayer.stats.runs}</span>
                    </div>
                    <div className="flex justify-between text-xl">
                      <span>Strike Rate:</span>
                      <span className="font-semibold">{currentPlayer.stats.strikeRate}</span>
                    </div>
                    <div className="flex justify-between text-xl">
                      <span>Average:</span>
                      <span className="font-semibold">{currentPlayer.stats.average}</span>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-800 rounded-lg p-6">
                  <h3 className="text-2xl font-semibold mb-4 text-gray-300">Bowling Stats</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between text-xl">
                      <span>Wickets:</span>
                      <span className="font-semibold">{currentPlayer.stats.wickets}</span>
                    </div>
                    <div className="flex justify-between text-xl">
                      <span>Economy:</span>
                      <span className="font-semibold">{currentPlayer.stats.economy}</span>
                    </div>
                    <div className="flex justify-between text-xl">
                      <span>Catches:</span>
                      <span className="font-semibold">{currentPlayer.stats.catches}</span>
                    </div>
                    <div className="flex justify-between text-xl">
                      <span>Style:</span>
                      <span className="font-semibold">{currentPlayer.bowlingStyle}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Auction Information */}
              <div className="bg-gray-800 rounded-lg p-6 mb-8">
                <h3 className="text-2xl font-semibold mb-4 text-gray-300">Auction Details</h3>
                <div className="grid grid-cols-3 gap-6">
                  <div>
                    <p className="text-lg text-gray-400">Base Price</p>
                    <p className="text-3xl font-bold text-green-400">{formatCurrency(currentPlayer.basePrice)}</p>
                  </div>
                  <div>
                    <p className="text-lg text-gray-400">Current Bid</p>
                    <p className="text-3xl font-bold text-yellow-400">
                      {currentPlayer.currentBid > 0 ? formatCurrency(currentPlayer.currentBid) : 'No Bids'}
                    </p>
                  </div>
                  <div>
                    <p className="text-lg text-gray-400">Previous Team</p>
                    <p className="text-xl font-semibold">{currentPlayer.previousTeam || 'N/A'}</p>
                  </div>
                </div>
              </div>

              {/* Sold Information */}
              {currentPlayer.status === 'sold' && currentPlayer.soldTo && (
                <div className="bg-green-900 rounded-lg p-6 mb-8">
                  <h3 className="text-2xl font-semibold mb-4 text-green-300">Sold!</h3>
                  <div className="flex items-center space-x-6">
                    <div>
                      <p className="text-lg text-green-400">Sold to:</p>
                      <p className="text-2xl font-bold">
                        {mockTeams.find(t => t.id === currentPlayer.soldTo)?.name}
                      </p>
                    </div>
                    <div>
                      <p className="text-lg text-green-400">Final Price:</p>
                      <p className="text-2xl font-bold">{formatCurrency(currentPlayer.soldPrice || 0)}</p>
                    </div>
                  </div>
                </div>
              )}
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Bidding Panel */}
        <div className="w-96 bg-gray-800 border-l border-gray-700 p-6">
          {currentPlayer.status === 'available' && (
            <div>
              <h3 className="text-2xl font-semibold mb-6">Place Bid</h3>
              
              {!isBidding ? (
                <button
                  onClick={() => setIsBidding(true)}
                  className="w-full bg-green-600 hover:bg-green-700 text-white py-4 px-6 rounded-lg text-xl font-semibold transition-colors duration-200"
                >
                  Start Bidding
                </button>
              ) : (
                <div className="space-y-6">
                  <div>
                    <label className="block text-lg font-medium text-gray-300 mb-3">
                      Select Team
                    </label>
                    <select
                      value={selectedTeam}
                      onChange={(e) => setSelectedTeam(e.target.value)}
                      className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                    >
                      <option value="">Choose a team</option>
                      {teamBudgets.map((budget) => (
                        <option key={budget.teamId} value={budget.teamId}>
                          {budget.teamName} (₹{budget.remainingBudget.toLocaleString()})
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-lg font-medium text-gray-300 mb-3">
                      Bid Amount
                    </label>
                    <input
                      type="number"
                      value={bidAmount}
                      onChange={(e) => setBidAmount(Number(e.target.value))}
                      min={currentPlayer.currentBid + 1000}
                      max={teamBudgets.find(t => t.teamId === selectedTeam)?.remainingBudget || 0}
                      className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                      placeholder={`Min: ${formatCurrency(currentPlayer.currentBid + 1000)}`}
                    />
                  </div>

                  <div className="space-y-3">
                    <button
                      onClick={handleBid}
                      disabled={!selectedTeam || bidAmount <= currentPlayer.currentBid}
                      className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white py-3 px-6 rounded-lg text-lg font-semibold transition-colors duration-200"
                    >
                      Place Bid
                    </button>
                    <button
                      onClick={() => setIsBidding(false)}
                      className="w-full bg-gray-600 hover:bg-gray-700 text-white py-3 px-6 rounded-lg text-lg font-semibold transition-colors duration-200"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Navigation Controls */}
          <div className="mt-8 space-y-4">
            <div className="flex space-x-3">
              <button
                onClick={handlePrevious}
                disabled={currentPlayerIndex === 0}
                className="flex-1 bg-gray-600 hover:bg-gray-700 disabled:bg-gray-800 disabled:cursor-not-allowed text-white py-3 px-4 rounded-lg font-semibold transition-colors duration-200"
              >
                Previous
              </button>
              <button
                onClick={handleNext}
                disabled={currentPlayerIndex === players.length - 1}
                className="flex-1 bg-gray-600 hover:bg-gray-700 disabled:bg-gray-800 disabled:cursor-not-allowed text-white py-3 px-4 rounded-lg font-semibold transition-colors duration-200"
              >
                Next
              </button>
            </div>
            
            <div className="text-center text-gray-400 text-sm">
              Use arrow keys or buttons to navigate
            </div>
            
            {/* Quick Stats */}
            <div className="mt-6 space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Available:</span>
                <span className="text-yellow-400 font-semibold">
                  {players.filter(p => p.status === 'available').length}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Sold:</span>
                <span className="text-green-400 font-semibold">
                  {players.filter(p => p.status === 'sold').length}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Unsold:</span>
                <span className="text-red-400 font-semibold">
                  {players.filter(p => p.status === 'unsold').length}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PlayerProjector
