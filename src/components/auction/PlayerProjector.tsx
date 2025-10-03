/**
 * PlayerProjector Component
 * Updated to use real player photos extracted from 2025-BCL-Players.pdf
 * Photos are stored in /src/assets/players/ with Mobile-Name.png format
 */
import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { mockTeams } from '@/data/mockData'
import { auctionPlayers } from '@/data/auctionPlayers'

interface AuctionPlayer {
  id: string
  name: string
  role: 'Batsman' | 'Bowler' | 'All Rounder' | 'Wicket Keeper'
  age: string
  mobile: string
  basePrice: number
  currentBid: number
  soldTo?: string
  soldPrice?: number
  status: 'available' | 'sold' | 'unsold'
  photo: string
  teamLogo?: string
  iconPlayer: string
}

interface TeamBudget {
  teamId: string
  teamName: string
  totalBudget: number
  spentAmount: number
  remainingBudget: number
  playersBought: number
  logo: string
}

interface PlayerProjectorProps {
  players: AuctionPlayer[]
  currentPlayerIndex: number
  onPlayerChange: (index: number) => void
  onBid: (playerId: string, teamId: string, amount: number) => void
  onPlayerUpdate?: (playerId: string, updates: Partial<AuctionPlayer>) => void
  teamBudgets: TeamBudget[]
  onBackToList?: () => void
}

function PlayerProjector({ 
  players, 
  currentPlayerIndex, 
  onPlayerChange, 
  onBid,
  onPlayerUpdate,
  teamBudgets,
  onBackToList
}: PlayerProjectorProps) {
  const [bidAmount, setBidAmount] = useState<number>(0)
  const [selectedTeam, setSelectedTeam] = useState<string>('')
  const [isBidding, setIsBidding] = useState<boolean>(false)
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false)
  const [imageLoading, setImageLoading] = useState<boolean>(true)
  const [imageError, setImageError] = useState<boolean>(false)
  const [isEditMode, setIsEditMode] = useState<boolean>(false)
  const [editForm, setEditForm] = useState<Partial<AuctionPlayer>>({})

  const currentPlayer = players[currentPlayerIndex]

  useEffect(() => {
    setBidAmount(currentPlayer?.basePrice || 0)
    setSelectedTeam('')
    setIsBidding(false)
    setImageLoading(true)
    setImageError(false)
    setIsEditMode(false)
    setEditForm({})
  }, [currentPlayer])

  // Fullscreen functionality
  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen()
      setIsFullscreen(true)
      // Hide body scrollbar and header when in fullscreen
      document.body.style.overflow = 'hidden'
      document.body.classList.add('projector-fullscreen')
    } else {
      document.exitFullscreen()
      setIsFullscreen(false)
      // Restore body scrollbar and header when exiting fullscreen
      document.body.style.overflow = 'auto'
      document.body.classList.remove('projector-fullscreen')
    }
  }

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      document.body.style.overflow = 'auto'
      document.body.classList.remove('projector-fullscreen')
    }
  }, [])

  // Keyboard navigation
  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      if (event.key === 'ArrowLeft' && currentPlayerIndex > 0) {
        handlePrevious()
      } else if (event.key === 'ArrowRight' && currentPlayerIndex < players.length - 1) {
        handleNext()
      } else if (event.key === 'Escape') {
        setIsBidding(false)
        setIsEditMode(false)
        if (isFullscreen) {
          document.exitFullscreen()
          setIsFullscreen(false)
        }
      } else if (event.key === 'e' && event.ctrlKey) {
        event.preventDefault()
        handleEditMode()
      } else if (event.key === 'F11') {
        event.preventDefault()
        toggleFullscreen()
      }
    }

    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [currentPlayerIndex, players.length, isFullscreen])

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount)
  }

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'Batsman':
        return 'bg-blue-600 text-white'
      case 'Bowler':
        return 'bg-red-600 text-white'
      case 'All Rounder':
        return 'bg-green-600 text-white'
      case 'Wicket Keeper':
        return 'bg-purple-600 text-white'
      default:
        return 'bg-gray-600 text-white'
    }
  }

  const getStatusColor = (status: 'available' | 'sold' | 'unsold') => {
    switch (status) {
      case 'available':
        return 'bg-yellow-500 text-gray-900'
      case 'sold':
        return 'bg-green-600 text-white'
      case 'unsold':
        return 'bg-red-600 text-white'
      default:
        return 'bg-gray-500 text-white'
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

  const handleBid = () => {
    if (currentPlayer && selectedTeam && bidAmount > currentPlayer.currentBid) {
      onBid(currentPlayer.id, selectedTeam, bidAmount)
      setIsBidding(false)
    } else {
      alert('Please select a team and enter a valid bid amount.')
    }
  }

  const getTeamName = (teamId: string) => {
    return teamBudgets.find(t => t.teamId === teamId)?.teamName || 'Unknown Team'
  }

  const getPlayerPhotoPath = (player: AuctionPlayer) => {
    // Use the photo path from the player data, or generate fallback
    return player.photo || `/src/assets/players/${player.mobile}-${player.name.replace(/[^\w\s-]/g, '').replace(/[-\s]+/g, '-').trim()}.png`
  }

  const handleEditMode = () => {
    if (currentPlayer) {
      setIsEditMode(true)
      setEditForm({
        name: currentPlayer.name,
        role: currentPlayer.role,
        age: currentPlayer.age,
        mobile: currentPlayer.mobile,
        basePrice: currentPlayer.basePrice,
        currentBid: currentPlayer.currentBid,
        status: currentPlayer.status,
        soldTo: currentPlayer.soldTo,
        soldPrice: currentPlayer.soldPrice,
        iconPlayer: currentPlayer.iconPlayer
      })
    }
  }

  const handleSaveEdit = () => {
    if (currentPlayer && onPlayerUpdate) {
      onPlayerUpdate(currentPlayer.id, editForm)
      setIsEditMode(false)
      setEditForm({})
    }
  }

  const handleCancelEdit = () => {
    setIsEditMode(false)
    setEditForm({})
  }

  if (!currentPlayer) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-900">
        <div className="text-white text-2xl">No players available</div>
      </div>
    )
  }

  return (
    <div className={`fixed inset-0 w-full h-full text-white overflow-hidden z-50 ${isFullscreen ? 'bg-black' : ''}`}>
      {/* Stadium Background */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `url('/src/assets/images/stadium-illustration.jpg')`,
          filter: 'brightness(0.3)'
        }}
      />
      
      {/* Overlay for better text readability */}
      <div className="absolute inset-0 bg-black bg-opacity-60" />
      
      {/* Projector Header */}
      <div className="relative bg-black bg-opacity-80 py-4 px-8 border-b border-gray-700">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <div className="text-2xl font-bold">BCL 2024 Player Auction</div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-lg">
              Player {currentPlayerIndex + 1} of {players.length}
            </div>
            <button
              onClick={handleEditMode}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2"
              title="Edit Player Info (Ctrl+E)"
            >
              <span className="material-icons text-lg">edit</span>
              <span>Edit</span>
            </button>
            <button
              onClick={toggleFullscreen}
              className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2"
              title="Toggle Fullscreen (F11)"
            >
              <span className="material-icons text-lg">
                {isFullscreen ? 'fullscreen_exit' : 'fullscreen'}
              </span>
              <span>{isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}</span>
            </button>
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

      {/* Main Projector Display - Split Layout matching image */}
      <div className="flex h-screen">
        {/* Left Section - Player Profile */}
        <div className="flex-1 p-8 relative z-10 flex flex-col justify-center">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentPlayer.id}
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 50 }}
              transition={{ duration: 0.5 }}
              className="max-w-md mx-auto"
            >
              {/* Player Photo */}
              <div className="mb-8 flex justify-center">
                <div className="w-48 h-48 rounded-2xl overflow-hidden border-4 border-white border-opacity-30 shadow-2xl relative">
                  {imageLoading && (
                    <div className="absolute inset-0 bg-gray-800 flex items-center justify-center">
                      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
                    </div>
                  )}
                  <img
                    src={getPlayerPhotoPath(currentPlayer)}
                    alt={currentPlayer.name}
                    className={`w-full h-full object-cover transition-opacity duration-300 ${imageLoading ? 'opacity-0' : 'opacity-100'}`}
                    onLoad={() => {
                      setImageLoading(false)
                      setImageError(false)
                    }}
                    onError={() => {
                      setImageLoading(false)
                      setImageError(true)
                    }}
                  />
                  {imageError && (
                    <div className="absolute inset-0 bg-gradient-to-br from-gray-700 to-gray-900 flex items-center justify-center text-6xl font-bold text-white">
                      {currentPlayer.name.split(' ').map(n => n[0]).join('')}
                    </div>
                  )}
                </div>
              </div>

              {/* Player Information - Matching Image Layout */}
              <div className="bg-black bg-opacity-40 backdrop-blur-sm rounded-2xl p-6 border border-white border-opacity-20">
                <div className="space-y-4">
                  {/* Name */}
                  <div className="flex justify-between items-center">
                    <span className="text-white text-lg font-medium">Name:</span>
                    <div className="flex items-center space-x-2">
                      <span className="text-white text-lg font-semibold">{currentPlayer.name}</span>
                      {currentPlayer.iconPlayer === 'Yes' && (
                        <span className="px-2 py-1 bg-yellow-500 text-yellow-900 text-xs font-bold rounded-full">
                          ICON
                        </span>
                      )}
                    </div>
                  </div>
                  
                  {/* Category */}
                  <div className="flex justify-between items-center">
                    <span className="text-white text-lg font-medium">Category:</span>
                    <span className={`px-3 py-1 rounded-lg text-sm font-semibold ${getRoleColor(currentPlayer.role)}`}>
                      {currentPlayer.role}
                    </span>
                  </div>
                  
                  {/* Age */}
                  <div className="flex justify-between items-center">
                    <span className="text-white text-lg font-medium">Age:</span>
                    <span className="text-white text-lg font-semibold">{currentPlayer.age} years</span>
                  </div>
                  
                  {/* Phone */}
                  <div className="flex justify-between items-center">
                    <span className="text-white text-lg font-medium">Ph:</span>
                    <span className="text-white text-lg font-semibold">{currentPlayer.mobile || 'N/A'}</span>
                  </div>
                </div>
              </div>

              {/* Navigation Controls */}
              <div className="flex justify-center space-x-4 mt-8">
                <button
                  onClick={handlePrevious}
                  disabled={currentPlayerIndex === 0}
                  className="bg-white bg-opacity-20 hover:bg-opacity-30 disabled:bg-opacity-10 disabled:cursor-not-allowed text-gray-600 px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center space-x-2 backdrop-blur-sm"
                >
                  <span className="material-icons">chevron_left</span>
                  <span>Previous</span>
                </button>
                <button
                  onClick={handleNext}
                  disabled={currentPlayerIndex === players.length - 1}
                  className="bg-white bg-opacity-20 hover:bg-opacity-30 disabled:bg-opacity-10 disabled:cursor-not-allowed text-gray-600 px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center space-x-2 backdrop-blur-sm"
                >
                  <span>Next</span>
                  <span className="material-icons">chevron_right</span>
                </button>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Right Section - BCL Tournament Branding */}
        <div className="w-96 bg-gradient-to-br from-green-500 to-green-600 relative z-10 flex flex-col justify-center items-center p-8">
          {currentPlayer?.status === 'sold' && currentPlayer?.teamLogo ? (
            <img 
              src={currentPlayer.teamLogo} 
              alt={`${getTeamName(currentPlayer.soldTo || '')} Logo`} 
              className="w-full h-auto rounded-lg shadow-lg"
              onError={(e) => {
                const target = e.target as HTMLImageElement
                target.style.display = 'none'
                target.nextElementSibling?.classList.remove('hidden')
              }}
            />
          ) : null}
          <img 
            src="/src/assets/images/slide-bcl-logo.png" 
            alt="BCL Logo" 
            className={`w-full h-auto ${currentPlayer?.status === 'sold' && currentPlayer?.teamLogo ? 'hidden' : ''}`} 
          />
  
          {/* Auction Details */}
          <div className="mt-8 w-full space-y-4">
            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="text-white text-sm mb-2">Base Price</div>
              <div className="text-white text-xl font-bold">{formatCurrency(currentPlayer.basePrice)}</div>
            </div>
            
            <div className="bg-black bg-opacity-30 rounded-lg p-4">
              <div className="text-white text-sm mb-2">Current Bid</div>
              <div className="text-yellow-300 text-xl font-bold">{formatCurrency(currentPlayer.currentBid)}</div>
            </div>
          </div>

          {/* Bidding Controls */}
          {currentPlayer.status === 'available' && (
            <div className="mt-8 w-full space-y-4">
              <div>
                <label className="block text-white text-sm mb-2">Bid Amount</label>
                <input
                  type="number"
                  value={bidAmount}
                  onChange={(e) => setBidAmount(Number(e.target.value))}
                  className="w-full px-4 py-2 bg-white bg-opacity-20 border border-white border-opacity-30 rounded-lg text-white placeholder-white placeholder-opacity-70 focus:ring-2 focus:ring-white focus:border-transparent"
                  min={currentPlayer.currentBid + 1000}
                  step="1000"
                />
              </div>

              <div>
                <label className="block text-white text-sm mb-2">Select Team</label>
                <select
                  value={selectedTeam}
                  onChange={(e) => setSelectedTeam(e.target.value)}
                  className="w-full px-4 py-2 bg-white bg-opacity-20 border border-white border-opacity-30 rounded-lg text-white focus:ring-2 focus:ring-white focus:border-transparent"
                >
                  <option value="">Choose a team</option>
                  {teamBudgets.map((team) => (
                    <option key={team.teamId} value={team.teamId} className="bg-gray-800">
                      {team.teamName} - {formatCurrency(team.remainingBudget)}
                    </option>
                  ))}
                </select>
              </div>

              <button
                onClick={handleBid}
                disabled={!selectedTeam || bidAmount <= currentPlayer.currentBid}
                className="w-full bg-white bg-opacity-20 hover:bg-opacity-30 disabled:bg-opacity-10 disabled:cursor-not-allowed text-white py-3 rounded-lg font-semibold transition-all duration-200 border border-white border-opacity-30"
              >
                Place Bid
              </button>
            </div>
          )}

          {/* Sold Status */}
          {currentPlayer.status === 'sold' && (
            <div className="mt-8 text-center">
              <div className="text-6xl mb-4">🏆</div>
              <div className="text-white text-xl font-semibold mb-2">Player Sold!</div>
              <div className="text-white text-lg">
                {currentPlayer.soldTo && getTeamName(currentPlayer.soldTo)}
              </div>
              <div className="text-yellow-300 text-2xl font-bold mt-2">
                {currentPlayer.soldPrice && formatCurrency(currentPlayer.soldPrice)}
              </div>
              {currentPlayer.teamLogo && (
                <div className="mt-4">
                  <img
                    src={currentPlayer.teamLogo}
                    alt={getTeamName(currentPlayer.soldTo || '')}
                    className="w-16 h-16 rounded-full object-cover mx-auto"
                  />
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Edit Modal */}
      {isEditMode && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-60 p-4">
          <div className="bg-white rounded-lg p-6 max-w-md w-full max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">Edit Player Information</h2>
              <button
                onClick={handleCancelEdit}
                className="text-gray-500 hover:text-gray-700"
              >
                <span className="material-icons">close</span>
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input
                  type="text"
                  value={editForm.name || ''}
                  onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
                <select
                  value={editForm.role || ''}
                  onChange={(e) => setEditForm({ ...editForm, role: e.target.value as any })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Batsman">Batsman</option>
                  <option value="Bowler">Bowler</option>
                  <option value="All Rounder">All Rounder</option>
                  <option value="Wicket Keeper">Wicket Keeper</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
                <input
                  type="text"
                  value={editForm.age || ''}
                  onChange={(e) => setEditForm({ ...editForm, age: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Mobile</label>
                <input
                  type="text"
                  value={editForm.mobile || ''}
                  onChange={(e) => setEditForm({ ...editForm, mobile: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Base Price</label>
                <input
                  type="number"
                  value={editForm.basePrice || ''}
                  onChange={(e) => setEditForm({ ...editForm, basePrice: parseInt(e.target.value) || 0 })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Current Bid</label>
                <input
                  type="number"
                  value={editForm.currentBid || ''}
                  onChange={(e) => setEditForm({ ...editForm, currentBid: parseInt(e.target.value) || 0 })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select
                  value={editForm.status || ''}
                  onChange={(e) => setEditForm({ ...editForm, status: e.target.value as any })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="available">Available</option>
                  <option value="sold">Sold</option>
                  <option value="unsold">Unsold</option>
                </select>
              </div>

              {editForm.status === 'sold' && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Sold To Team</label>
                    <select
                      value={editForm.soldTo || ''}
                      onChange={(e) => setEditForm({ ...editForm, soldTo: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">Select Team</option>
                      {teamBudgets.map((team) => (
                        <option key={team.teamId} value={team.teamId}>
                          {team.teamName}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Sold Price</label>
                    <input
                      type="number"
                      value={editForm.soldPrice || ''}
                      onChange={(e) => setEditForm({ ...editForm, soldPrice: parseInt(e.target.value) || 0 })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Icon Player</label>
                <select
                  value={editForm.iconPlayer || ''}
                  onChange={(e) => setEditForm({ ...editForm, iconPlayer: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
            </div>

            <div className="flex space-x-3 mt-6">
              <button
                onClick={handleSaveEdit}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md font-medium transition-colors duration-200"
              >
                Save Changes
              </button>
              <button
                onClick={handleCancelEdit}
                className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-700 py-2 px-4 rounded-md font-medium transition-colors duration-200"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default PlayerProjector