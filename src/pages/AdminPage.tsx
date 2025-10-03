import { useState } from 'react'
import { motion } from 'framer-motion'
import { mockAuctionPlayers, mockTeams, mockTeamBudgets } from '@/data/mockData'
import { AuctionPlayer, TeamBudget } from '@/types'

function AdminPage() {
  const [players, setPlayers] = useState<AuctionPlayer[]>(mockAuctionPlayers)
  const [teamBudgets, setTeamBudgets] = useState<TeamBudget[]>(mockTeamBudgets)
  const [selectedPlayer, setSelectedPlayer] = useState<AuctionPlayer | null>(null)
  const [isEditing, setIsEditing] = useState<boolean>(false)
  const [editForm, setEditForm] = useState({
    basePrice: 0,
    currentBid: 0,
    status: 'available' as 'available' | 'sold' | 'unsold',
    soldTo: '',
    soldPrice: 0
  })

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

  const handleEditPlayer = (player: AuctionPlayer) => {
    setSelectedPlayer(player)
    setEditForm({
      basePrice: player.basePrice,
      currentBid: player.currentBid,
      status: player.status,
      soldTo: player.soldTo || '',
      soldPrice: player.soldPrice || 0
    })
    setIsEditing(true)
  }

  const handleSavePlayer = () => {
    if (!selectedPlayer) return

    const updatedPlayers = players.map(player => {
      if (player.id === selectedPlayer.id) {
        return {
          ...player,
          basePrice: editForm.basePrice,
          currentBid: editForm.currentBid,
          status: editForm.status,
          soldTo: editForm.status === 'sold' ? editForm.soldTo : undefined,
          soldPrice: editForm.status === 'sold' ? editForm.soldPrice : undefined
        }
      }
      return player
    })

    setPlayers(updatedPlayers)
    setIsEditing(false)
    setSelectedPlayer(null)
  }

  const handleCancelEdit = () => {
    setIsEditing(false)
    setSelectedPlayer(null)
  }

  const handleBulkAction = (action: 'reset' | 'markUnsold') => {
    if (action === 'reset') {
      setPlayers(mockAuctionPlayers)
      setTeamBudgets(mockTeamBudgets)
    } else if (action === 'markUnsold') {
      const updatedPlayers = players.map(player => ({
        ...player,
        status: 'unsold' as const,
        soldTo: undefined,
        soldPrice: undefined
      }))
      setPlayers(updatedPlayers)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Auction Admin Panel</h1>
              <p className="text-gray-600 mt-1">Manage player prices and team assignments</p>
            </div>
            <div className="flex space-x-3">
              <button
                onClick={() => handleBulkAction('markUnsold')}
                className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200"
              >
                Mark All Unsold
              </button>
              <button
                onClick={() => handleBulkAction('reset')}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200"
              >
                Reset Auction
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Players List */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900">Players ({players.length})</h2>
              </div>
              <div className="divide-y divide-gray-200">
                {players.map((player) => (
                  <motion.div
                    key={player.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="p-6 hover:bg-gray-50 transition-colors duration-200"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
                          <span className="text-lg font-bold text-gray-600">
                            {player.name.split(' ').map(n => n[0]).join('')}
                          </span>
                        </div>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">{player.name}</h3>
                          <div className="flex items-center space-x-3 mt-1">
                            <span className={`px-2 py-1 rounded text-sm font-medium ${getRoleColor(player.role)}`}>
                              {player.role}
                            </span>
                            <span className={`px-2 py-1 rounded text-sm font-medium ${getStatusColor(player.status)}`}>
                              {player.status.toUpperCase()}
                            </span>
                            <span className="text-sm text-gray-600">Age: {player.age}</span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-6">
                        <div className="text-right">
                          <p className="text-sm text-gray-600">Base Price</p>
                          <p className="font-semibold text-green-600">{formatCurrency(player.basePrice)}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm text-gray-600">Current Bid</p>
                          <p className="font-semibold text-blue-600">
                            {player.currentBid > 0 ? formatCurrency(player.currentBid) : 'No Bids'}
                          </p>
                        </div>
                        {player.status === 'sold' && player.soldTo && (
                          <div className="text-right">
                            <p className="text-sm text-gray-600">Sold To</p>
                            <p className="font-semibold text-purple-600">
                              {mockTeams.find(t => t.id === player.soldTo)?.name}
                            </p>
                          </div>
                        )}
                        <button
                          onClick={() => handleEditPlayer(player)}
                          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
                        >
                          Edit
                        </button>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>

          {/* Team Budgets */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">Team Budgets</h3>
              </div>
              <div className="p-6 space-y-4">
                {teamBudgets.map((budget) => (
                  <div key={budget.teamId} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium text-gray-900">{budget.teamName}</span>
                      <span className="text-sm text-gray-600">{budget.playersBought} players</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                      <div
                        className="bg-green-500 h-2 rounded-full"
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

            {/* Quick Stats */}
            <div className="bg-white rounded-lg shadow-sm">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">Auction Stats</h3>
              </div>
              <div className="p-6 space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Players:</span>
                  <span className="font-semibold">{players.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Sold:</span>
                  <span className="font-semibold text-green-600">
                    {players.filter(p => p.status === 'sold').length}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Available:</span>
                  <span className="font-semibold text-yellow-600">
                    {players.filter(p => p.status === 'available').length}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Unsold:</span>
                  <span className="font-semibold text-red-600">
                    {players.filter(p => p.status === 'unsold').length}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Amount:</span>
                  <span className="font-semibold">
                    {formatCurrency(players.reduce((sum, p) => sum + (p.soldPrice || 0), 0))}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Edit Modal */}
      {isEditing && selectedPlayer && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4"
          >
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Edit Player: {selectedPlayer.name}</h3>
            </div>
            
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Base Price
                </label>
                <input
                  type="number"
                  value={editForm.basePrice}
                  onChange={(e) => setEditForm({ ...editForm, basePrice: Number(e.target.value) })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Current Bid
                </label>
                <input
                  type="number"
                  value={editForm.currentBid}
                  onChange={(e) => setEditForm({ ...editForm, currentBid: Number(e.target.value) })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Status
                </label>
                <select
                  value={editForm.status}
                  onChange={(e) => setEditForm({ ...editForm, status: e.target.value as any })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="available">Available</option>
                  <option value="sold">Sold</option>
                  <option value="unsold">Unsold</option>
                </select>
              </div>

              {editForm.status === 'sold' && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Sold To Team
                    </label>
                    <select
                      value={editForm.soldTo}
                      onChange={(e) => setEditForm({ ...editForm, soldTo: e.target.value })}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">Select Team</option>
                      {mockTeams.map(team => (
                        <option key={team.id} value={team.id}>{team.name}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Sold Price
                    </label>
                    <input
                      type="number"
                      value={editForm.soldPrice}
                      onChange={(e) => setEditForm({ ...editForm, soldPrice: Number(e.target.value) })}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </>
              )}
            </div>

            <div className="px-6 py-4 border-t border-gray-200 flex justify-end space-x-3">
              <button
                onClick={handleCancelEdit}
                className="px-4 py-2 text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-lg font-medium transition-colors duration-200"
              >
                Cancel
              </button>
              <button
                onClick={handleSavePlayer}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-200"
              >
                Save Changes
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  )
}

export default AdminPage
