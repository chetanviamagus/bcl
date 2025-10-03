import { useState } from 'react'
import { motion } from 'framer-motion'
import { mockAuctionPlayers, mockAuctionSession, mockTeamBudgets, mockTeams } from '@/data/mockData'
import { AuctionPlayer, TeamBudget } from '@/types'
import PlayerProjector from '@/components/auction/PlayerProjector'

function AuctionPage() {
  const [selectedPlayer, setSelectedPlayer] = useState<AuctionPlayer | null>(null)
  const [bidAmount, setBidAmount] = useState<number>(0)
  const [selectedTeam, setSelectedTeam] = useState<string>('')
  const [players, setPlayers] = useState<AuctionPlayer[]>(mockAuctionPlayers)
  const [teamBudgets, setTeamBudgets] = useState<TeamBudget[]>(mockTeamBudgets)
  const [viewMode, setViewMode] = useState<'list' | 'projector'>('list')
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState<number>(0)

  const handleBid = (playerId: string, teamId: string, amount: number) => {
    const updatedPlayers = players.map(player => {
      if (player.id === playerId) {
        return {
          ...player,
          currentBid: amount,
          soldTo: teamId,
          status: 'sold' as const,
          soldPrice: amount
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
  }

  const handlePlayerChange = (index: number) => {
    setCurrentPlayerIndex(index)
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
      'Batsman': 'bg-green-100 text-green-800',
      'Bowler': 'bg-red-100 text-red-800',
      'All-rounder': 'bg-blue-100 text-blue-800',
      'Wicket-keeper': 'bg-purple-100 text-purple-800'
    }
    return colors[role as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  const getStatusColor = (status: string) => {
    const colors = {
      'available': 'bg-yellow-100 text-yellow-800',
      'sold': 'bg-green-100 text-green-800',
      'unsold': 'bg-red-100 text-red-800'
    }
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  // Show projector view if in projector mode
  if (viewMode === 'projector') {
    return (
      <PlayerProjector
        players={players}
        currentPlayerIndex={currentPlayerIndex}
        onPlayerChange={handlePlayerChange}
        onBid={handleBid}
        teamBudgets={teamBudgets}
        onBackToList={() => setViewMode('list')}
      />
    )
  }

  return (
    <div className="min-h-screen bg-cricket-light">
      {/* Header Section */}
      <div className="bg-cricket-green text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-2">{mockAuctionSession.name}</h1>
            <p className="text-xl mb-4">
              {mockAuctionSession.date} • {mockAuctionSession.startTime} - {mockAuctionSession.endTime}
            </p>
            <div className="flex justify-center space-x-8 text-sm">
              <div>
                <span className="font-semibold">Total Players:</span> {mockAuctionSession.totalPlayers}
              </div>
              <div>
                <span className="font-semibold">Sold:</span> {mockAuctionSession.soldPlayers}
              </div>
              <div>
                <span className="font-semibold">Total Amount:</span> {formatCurrency(mockAuctionSession.totalAmount)}
              </div>
            </div>
            <div className="mt-4">
              <button
                onClick={() => setViewMode('projector')}
                className="bg-white text-cricket-green px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200"
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
            <h2 className="text-2xl font-bold text-cricket-dark mb-6">Available Players</h2>
            <div className="space-y-4">
              {players.map((player) => (
                <motion.div
                  key={player.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300"
                >
                  <div className="flex items-start space-x-4">
                    <div className="w-16 h-16 bg-cricket-light rounded-full flex items-center justify-center">
                      <span className="text-2xl font-bold text-cricket-green">
                        {player.name.split(' ').map(n => n[0]).join('')}
                      </span>
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-xl font-semibold text-cricket-dark">{player.name}</h3>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(player.status)}`}>
                          {player.status.toUpperCase()}
                        </span>
                      </div>
                      <div className="flex items-center space-x-4 mb-3">
                        <span className={`px-2 py-1 rounded text-sm font-medium ${getRoleColor(player.role)}`}>
                          {player.role}
                        </span>
                        <span className="text-sm text-gray-600">Age: {player.age}</span>
                        <span className="text-sm text-gray-600">{player.nationality}</span>
                      </div>
                      <div className="grid grid-cols-2 gap-4 mb-4">
                        <div>
                          <p className="text-sm text-gray-600">Base Price</p>
                          <p className="font-semibold text-cricket-green">{formatCurrency(player.basePrice)}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Current Bid</p>
                          <p className="font-semibold text-cricket-gold">
                            {player.currentBid > 0 ? formatCurrency(player.currentBid) : 'No Bids'}
                          </p>
                        </div>
                      </div>
                      {player.status === 'available' && (
                        <button
                          onClick={() => setSelectedPlayer(player)}
                          className="bg-cricket-green text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors duration-200"
                        >
                          Place Bid
                        </button>
                      )}
                      {player.status === 'sold' && player.soldTo && (
                        <div className="text-sm text-gray-600">
                          Sold to <span className="font-semibold">{mockTeams.find(t => t.id === player.soldTo)?.name}</span> for {formatCurrency(player.soldPrice || 0)}
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
              <h3 className="text-xl font-semibold text-cricket-dark mb-4">Team Budgets</h3>
              <div className="space-y-3">
                {teamBudgets.map((budget) => (
                  <div key={budget.teamId} className="border-b border-gray-200 pb-3 last:border-b-0">
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-medium text-cricket-dark">{budget.teamName}</span>
                      <span className="text-sm text-gray-600">{budget.playersBought} players</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 mb-1">
                      <div
                        className="bg-cricket-green h-2 rounded-full"
                        style={{ width: `${(budget.spentAmount / budget.totalBudget) * 100}%` }}
                      ></div>
                    </div>
                    <div className="flex justify-between text-sm text-gray-600">
                      <span>Spent: {formatCurrency(budget.spentAmount)}</span>
                      <span>Remaining: {formatCurrency(budget.remainingBudget)}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Bidding Panel */}
            {selectedPlayer && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold text-cricket-dark mb-4">Place Bid</h3>
                <div className="space-y-4">
                  <div>
                    <p className="text-sm text-gray-600">Player</p>
                    <p className="font-semibold">{selectedPlayer.name}</p>
                    <p className="text-sm text-gray-600">Base Price: {formatCurrency(selectedPlayer.basePrice)}</p>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Select Team
                    </label>
                    <select
                      value={selectedTeam}
                      onChange={(e) => setSelectedTeam(e.target.value)}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cricket-green"
                    >
                      <option value="">Choose a team</option>
                      {teamBudgets.map((budget) => (
                        <option key={budget.teamId} value={budget.teamId}>
                          {budget.teamName} (Remaining: {formatCurrency(budget.remainingBudget)})
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Bid Amount
                    </label>
                    <input
                      type="number"
                      value={bidAmount}
                      onChange={(e) => setBidAmount(Number(e.target.value))}
                      min={selectedPlayer.currentBid + 1000}
                      max={teamBudgets.find(t => t.teamId === selectedTeam)?.remainingBudget || 0}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-cricket-green"
                      placeholder={`Min: ${formatCurrency(selectedPlayer.currentBid + 1000)}`}
                    />
                  </div>

                  <div className="flex space-x-3">
                    <button
                      onClick={() => {
                        if (selectedTeam && bidAmount > selectedPlayer.currentBid) {
                          handleBid(selectedPlayer.id, selectedTeam, bidAmount)
                          setSelectedPlayer(null)
                        }
                      }}
                      disabled={!selectedTeam || bidAmount <= selectedPlayer.currentBid}
                      className="flex-1 bg-cricket-green text-white py-2 px-4 rounded-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors duration-200"
                    >
                      Place Bid
                    </button>
                    <button
                      onClick={() => setSelectedPlayer(null)}
                      className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-400 transition-colors duration-200"
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
