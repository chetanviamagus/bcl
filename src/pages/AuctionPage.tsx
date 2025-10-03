import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { mockTeams } from '@/data/mockData'
import { players as playersData } from '@/data/players_data'
import PlayerProjector from '@/components/auction/PlayerProjector'

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

const teamLogos = {
  'mr-titans': '/src/assets/images/team_logos/mr-titans.jpeg',
  'bellandur-monsters': '/src/assets/images/team_logos/bellandur-monsters.jpeg',
  'ykr-cricketers': '/src/assets/images/team_logos/ykr-cricketers.jpeg',
  'bellandur-sharks-cricketers': '/src/assets/images/team_logos/bellandur-sharks-cricketers.jpeg',
  'super-giants-bellandur': '/src/assets/images/team_logos/super-giants-bellandur.jpeg',
  'royal-challengers-bellandur': '/src/assets/images/team_logos/royal-challengers-bellandur.jpeg'
}

function AuctionPage() {
  const [selectedPlayer, setSelectedPlayer] = useState<AuctionPlayer | null>(null)
  const [bidAmount, setBidAmount] = useState<number>(0)
  const [selectedTeam, setSelectedTeam] = useState<string>('')
  const [players, setPlayers] = useState<AuctionPlayer[]>([])
  const [teamBudgets, setTeamBudgets] = useState<TeamBudget[]>([])
  const [viewMode, setViewMode] = useState<'list' | 'projector'>('list')
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState<number>(0)
  const [filterIconPlayers, setFilterIconPlayers] = useState<boolean>(false)

  // Initialize players from real data
  useEffect(() => {
    const auctionPlayers: AuctionPlayer[] = playersData.map((player, index) => ({
      id: `player-${index + 1}`,
      name: player.name,
      role: player.category as 'Batsman' | 'Bowler' | 'All Rounder' | 'Wicket Keeper',
      age: player.age,
      mobile: player.mobile,
      basePrice: Math.max(50000, Math.floor(Math.random() * 200000) + 50000), // Random base price between 50k-250k
      currentBid: 0,
      status: 'available' as const,
      photo: `/src/assets/players/${player.mobile}-${player.name.replace(/[^\w\s-]/g, '').replace(/[-\s]+/g, '-').trim()}.png`,
      iconPlayer: player.iconPlayer,
      teamLogo: undefined
    }))
    setPlayers(auctionPlayers)
  }, [])

  // Initialize team budgets
  useEffect(() => {
    const budgets: TeamBudget[] = mockTeams.map(team => ({
      teamId: team.id,
      teamName: team.name,
      totalBudget: 2000000, // 20 lakh budget per team
      spentAmount: 0,
      remainingBudget: 2000000,
      playersBought: 0,
      logo: teamLogos[team.id as keyof typeof teamLogos] || ''
    }))
    setTeamBudgets(budgets)
  }, [])

  const handleBid = (playerId: string, teamId: string, amount: number) => {
    const updatedPlayers = players.map(player => {
      if (player.id === playerId) {
        const team = teamBudgets.find(t => t.teamId === teamId)
        return {
          ...player,
          currentBid: amount,
          soldTo: teamId,
          status: 'sold' as const,
          soldPrice: amount,
          teamLogo: team?.logo || teamLogos[teamId as keyof typeof teamLogos] || ''
        }
      }
      return player
    })

    const updatedBudgets = teamBudgets.map(budget => {
      if (budget.teamId === teamId) {
        return {
          ...budget,
          spentAmount: budget.spentAmount + amount,
          remainingBudget: budget.remainingBudget - amount,
          playersBought: budget.playersBought + 1
        }
      }
      return budget
    })

    setPlayers(updatedPlayers)
    setTeamBudgets(updatedBudgets)
    setBidAmount(0)
    setSelectedTeam('')
    setSelectedPlayer(null)
  }

  const handlePlayerChange = (index: number) => {
    setCurrentPlayerIndex(index)
  }

  const handlePlayerUpdate = (playerId: string, updates: Partial<AuctionPlayer>) => {
    setPlayers(prevPlayers => 
      prevPlayers.map(player => 
        player.id === playerId ? { ...player, ...updates } : player
      )
    )
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount)
  }

  const getRoleColor = (role: string) => {
    const colors = {
      'Batsman': 'bg-green-600 text-white',
      'Bowler': 'bg-red-600 text-white',
      'All Rounder': 'bg-blue-600 text-white',
      'Wicket Keeper': 'bg-purple-600 text-white'
    }
    return colors[role as keyof typeof colors] || 'bg-gray-600 text-white'
  }

  const getStatusColor = (status: string) => {
    const colors = {
      'available': 'bg-yellow-500 text-gray-900',
      'sold': 'bg-green-600 text-white',
      'unsold': 'bg-red-600 text-white'
    }
    return colors[status as keyof typeof colors] || 'bg-gray-600 text-white'
  }

  const getTeamName = (teamId: string) => {
    return teamBudgets.find(t => t.teamId === teamId)?.teamName || 'Unknown Team'
  }

  // Show projector view if in projector mode
  if (viewMode === 'projector') {
    return (
      <PlayerProjector
        players={players}
        currentPlayerIndex={currentPlayerIndex}
        onPlayerChange={handlePlayerChange}
        onBid={handleBid}
        onPlayerUpdate={handlePlayerUpdate}
        teamBudgets={teamBudgets}
        onBackToList={() => setViewMode('list')}
      />
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header Section */}
      <div className="bg-green-600 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-2 text-white">BCL 2024 Player Auction</h1>
            <p className="text-xl mb-4 text-white/90">
              December 15, 2024 • 10:00 AM - 6:00 PM
            </p>
            <div className="flex justify-center space-x-8 text-sm text-white/90">
              <div>
                <span className="font-semibold">Total Players:</span> {players.length}
              </div>
              <div>
                <span className="font-semibold">ICON Players:</span> {players.filter(p => p.iconPlayer === 'Yes').length}
              </div>
              <div>
                <span className="font-semibold">Sold:</span> {players.filter(p => p.status === 'sold').length}
              </div>
              <div>
                <span className="font-semibold">Total Amount:</span> {formatCurrency(players.filter(p => p.status === 'sold').reduce((sum, p) => sum + (p.soldPrice || 0), 0))}
              </div>
            </div>
            <div className="mt-4">
              <button
                onClick={() => setViewMode('projector')}
                className="bg-white text-green-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-50 hover:shadow-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-green-600"
              >
                Switch to Projector View
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Players List */}
          <div className="lg:col-span-2">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Available Players</h2>
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="filterIcon"
                  checked={filterIconPlayers}
                  onChange={(e) => setFilterIconPlayers(e.target.checked)}
                  className="w-4 h-4 text-green-600 bg-gray-100 border-gray-300 rounded focus:ring-green-500"
                />
                <label htmlFor="filterIcon" className="text-sm font-medium text-gray-700">
                  Show only ICON players
                </label>
              </div>
            </div>
            <div className="space-y-4">
              {players
                .filter(player => !filterIconPlayers || player.iconPlayer === 'Yes')
                .map((player) => (
                <motion.div
                  key={player.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300"
                >
                  <div className="flex items-start space-x-4">
                    <div className="w-16 h-16 rounded-full overflow-hidden bg-gray-100">
                      <img
                        src={player.photo}
                        alt={player.name}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          const target = e.target as HTMLImageElement
                          target.style.display = 'none'
                          target.nextElementSibling?.classList.remove('hidden')
                        }}
                      />
                      <div className="w-full h-full bg-gray-200 flex items-center justify-center text-2xl font-bold text-green-600 hidden">
                        {player.name.split(' ').map(n => n[0]).join('')}
                      </div>
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <h3 className="text-xl font-semibold text-gray-900">{player.name}</h3>
                          {player.iconPlayer === 'Yes' && (
                            <span className="px-2 py-1 bg-yellow-500 text-yellow-900 text-xs font-bold rounded-full">
                              ICON
                            </span>
                          )}
                        </div>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(player.status)}`}>
                          {player.status.toUpperCase()}
                        </span>
                      </div>
                      <div className="flex items-center space-x-4 mb-3">
                        <span className={`px-2 py-1 rounded text-sm font-medium ${getRoleColor(player.role)}`}>
                          {player.role}
                        </span>
                        <span className="text-sm text-gray-600">Age: {player.age}</span>
                        <span className="text-sm text-gray-600">Ph: {player.mobile}</span>
                      </div>
                      <div className="grid grid-cols-2 gap-4 mb-4">
                        <div>
                          <p className="text-sm text-gray-600">Base Price</p>
                          <p className="font-bold text-lg text-green-600">{formatCurrency(player.basePrice)}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Current Bid</p>
                          <p className="font-bold text-lg text-yellow-600">
                            {player.currentBid > 0 ? formatCurrency(player.currentBid) : 'No Bids'}
                          </p>
                        </div>
                      </div>
                      {player.status === 'available' && (
                        <button
                          onClick={() => setSelectedPlayer(player)}
                          className="bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-700 hover:shadow-lg transform hover:scale-105 transition-all duration-200"
                        >
                          Place Bid
                        </button>
                      )}
                      {player.status === 'sold' && player.soldTo && (
                        <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                          <div className="flex items-center space-x-3">
                            <div className="text-sm text-green-800">
                              <span className="font-semibold">SOLD</span> to <span className="font-bold text-green-900">{getTeamName(player.soldTo)}</span> for <span className="font-bold text-green-900">{formatCurrency(player.soldPrice || 0)}</span>
                            </div>
                            {player.teamLogo && player.teamLogo !== '' ? (
                              <img
                                src={player.teamLogo}
                                alt={getTeamName(player.soldTo)}
                                className="w-8 h-8 rounded-full object-cover"
                                onError={(e) => {
                                  const target = e.target as HTMLImageElement
                                  target.style.display = 'none'
                                  target.nextElementSibling?.classList.remove('hidden')
                                }}
                              />
                            ) : (
                              <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center text-xs font-bold text-gray-600 hidden">
                                {getTeamName(player.soldTo).split(' ').map(n => n[0]).join('')}
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Team Budgets & Bidding Panel */}
          <div className="space-y-6">
            {/* Team Budgets */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Team Budgets</h3>
              <div className="space-y-3">
                {teamBudgets.map((budget) => (
                  <div key={budget.teamId} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200">
                    <div className="flex items-center space-x-3 mb-2">
                      {budget.logo ? (
                        <img
                          src={budget.logo}
                          alt={budget.teamName}
                          className="w-8 h-8 rounded-full object-cover"
                          onError={(e) => {
                            const target = e.target as HTMLImageElement
                            target.style.display = 'none'
                            target.nextElementSibling?.classList.remove('hidden')
                          }}
                        />
                      ) : null}
                      <div className={`w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center text-xs font-bold text-gray-600 ${budget.logo ? 'hidden' : ''}`}>
                        {budget.teamName.split(' ').map(n => n[0]).join('')}
                      </div>
                      <div className="flex-1">
                        <span className="font-semibold text-gray-900">{budget.teamName}</span>
                        <span className="text-sm font-medium text-blue-600 bg-blue-100 px-2 py-1 rounded-full ml-2">{budget.playersBought} players</span>
                      </div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
                      <div
                        className="bg-gradient-to-r from-green-500 to-green-400 h-3 rounded-full transition-all duration-300"
                        style={{ width: `${(budget.spentAmount / budget.totalBudget) * 100}%` }}
                      ></div>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Spent: <span className="font-semibold text-red-600">{formatCurrency(budget.spentAmount)}</span></span>
                      <span className="text-gray-600">Remaining: <span className="font-semibold text-green-600">{formatCurrency(budget.remainingBudget)}</span></span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Bidding Panel */}
            {selectedPlayer && (
              <div className="bg-gradient-to-br from-white to-gray-50 rounded-lg shadow-lg border border-gray-200 p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Place Bid</h3>
                <div className="space-y-4">
                  <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-sm text-gray-600">Player</p>
                    <p className="font-bold text-lg text-gray-900">{selectedPlayer.name}</p>
                    <p className="text-sm text-gray-600">Base Price: <span className="font-semibold text-green-600">{formatCurrency(selectedPlayer.basePrice)}</span></p>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-900 mb-3">
                      Select Team
                    </label>
                    <div className="grid grid-cols-2 gap-3">
                      {teamBudgets.map((budget) => (
                        <button
                          key={budget.teamId}
                          onClick={() => setSelectedTeam(budget.teamId)}
                          className={`p-3 rounded-lg border-2 transition-all duration-200 ${
                            selectedTeam === budget.teamId
                              ? 'border-green-500 bg-green-50'
                              : 'border-gray-300 hover:border-gray-400'
                          }`}
                        >
                          <div className="flex flex-col items-center space-y-2">
                            <img
                              src={budget.logo}
                              alt={budget.teamName}
                              className="w-12 h-12 rounded-full object-cover"
                            />
                            <div className="text-center">
                              <p className="text-sm font-medium text-gray-900">{budget.teamName}</p>
                              <p className="text-xs text-gray-600">{formatCurrency(budget.remainingBudget)} left</p>
                            </div>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-900 mb-2">
                      Bid Amount
                    </label>
                    <input
                      type="number"
                      value={bidAmount}
                      onChange={(e) => setBidAmount(Number(e.target.value))}
                      min={selectedPlayer.currentBid + 1000}
                      max={teamBudgets.find(t => t.teamId === selectedTeam)?.remainingBudget || 0}
                      className="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors duration-200"
                      placeholder={`Min: ${formatCurrency(selectedPlayer.currentBid + 1000)}`}
                    />
                  </div>

                  <div className="flex space-x-3">
                    <button
                      onClick={() => {
                        if (selectedTeam && bidAmount > selectedPlayer.currentBid) {
                          handleBid(selectedPlayer.id, selectedTeam, bidAmount)
                        }
                      }}
                      disabled={!selectedTeam || bidAmount <= selectedPlayer.currentBid}
                      className="flex-1 bg-green-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-green-700 hover:shadow-lg transform hover:scale-105 disabled:bg-gray-300 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-none transition-all duration-200"
                    >
                      Place Bid
                    </button>
                    <button
                      onClick={() => setSelectedPlayer(null)}
                      className="flex-1 bg-gray-500 text-white py-3 px-6 rounded-lg font-semibold hover:bg-gray-600 hover:shadow-lg transform hover:scale-105 transition-all duration-200"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AuctionPage