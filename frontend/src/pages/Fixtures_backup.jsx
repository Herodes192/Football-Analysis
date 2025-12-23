import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Calendar, Target, TrendingUp, AlertTriangle, X, Shield, Users, Clock, Zap } from 'lucide-react'

const Fixtures = () => {
  const [selectedMatch, setSelectedMatch] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [loadingAnalysis, setLoadingAnalysis] = useState(false)
  
  const { data, isLoading, error } = useQuery({
    queryKey: ['allFixtures'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/v1/fixtures/all')
      return res.json()
    }
  })

  const handleMatchClick = async (fixture) => {
    if (fixture.status === 'finished') return
    
    setSelectedMatch(fixture)
    setLoadingAnalysis(true)
    setAnalysis(null)
    
    try {
      const res = await fetch(
        `http://localhost:8000/api/v1/match-analysis/${fixture.opponent_id}?opponent_name=${encodeURIComponent(fixture.opponent_name)}`
      )
      const data = await res.json()
      setAnalysis(data)
    } catch (err) {
      console.error('Error fetching analysis:', err)
    } finally {
      setLoadingAnalysis(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading fixtures...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border-l-4 border-red-500 p-4">
        <p className="text-red-700">Error loading fixtures: {error.message}</p>
      </div>
    )
  }

  const fixtures = data?.fixtures || []
  const upcomingCount = data?.upcoming_count || 0

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Fixtures</h2>
          <p className="text-gray-600 mt-2">
            {upcomingCount} upcoming matches - Click upcoming fixtures for tactical analysis
          </p>
        </div>
        <div className="bg-blue-100 px-4 py-2 rounded-lg">
          <p className="text-sm text-blue-700 font-medium">Liga Portugal 2025/26</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-3">
        {fixtures.map((fixture) => {
          const matchDate = new Date(fixture.date)
          const isUpcoming = fixture.status === 'upcoming'
          const locationClass = fixture.is_home ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'
          
          let resultClass = ''
          if (fixture.result === 'W') resultClass = 'bg-green-500 text-white'
          else if (fixture.result === 'L') resultClass = 'bg-red-500 text-white'
          else if (fixture.result === 'D') resultClass = 'bg-gray-400 text-white'
          
          return (
            <div
              key={fixture.id}
              onClick={() => isUpcoming && handleMatchClick(fixture)}
              className={`bg-white rounded-lg shadow-md p-4 transition-all duration-300 border-2 ${
                isUpcoming 
                  ? 'hover:shadow-xl cursor-pointer border-transparent hover:border-blue-500' 
                  : 'border-gray-200 opacity-75'
              }`}
            >
              <div className="flex items-center justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3">
                    <div className="font-bold text-gray-900 truncate">
                      Gil Vicente
                    </div>
                    <span className="text-2xl text-gray-400">vs</span>
                    <div className="font-bold text-gray-900 truncate">
                      {fixture.opponent_name}
                    </div>
                    {!isUpcoming && fixture.score && (
                      <div className={`px-3 py-1 rounded-lg font-bold ${resultClass}`}>
                        {fixture.score.display}
                      </div>
                    )}
                  </div>
                  <div className="flex items-center gap-3 mt-2 text-xs text-gray-600">
                    <span className="flex items-center gap-1">
                      <Calendar size={14} />
                      {matchDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                    </span>
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${locationClass}`}>
                      {fixture.is_home ? '🏠' : '✈️'} {fixture.is_home ? 'HOME' : 'AWAY'}
                    </span>
                    {!isUpcoming && fixture.result && (
                      <span className={`px-2 py-1 rounded-full text-xs font-bold ${resultClass}`}>
                        {fixture.result === 'W' ? '✓ WIN' : fixture.result === 'L' ? '✗ LOSS' : '- DRAW'}
                      </span>
                    )}
                  </div>
                </div>
                {isUpcoming && (
                  <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 transition-colors flex items-center gap-2 shrink-0">
                    <Target size={16} />
                    Analyze
                  </button>
                )}
              </div>
            </div>
          )
        })}
      </div>

      {selectedMatch && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto">
          <div className="bg-white rounded-xl shadow-2xl max-w-5xl w-full my-8">
            <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 flex items-center justify-between rounded-t-xl">
              <div>
                <h3 className="text-2xl font-bold">Tactical Analysis</h3>
                <p className="text-blue-100">Gil Vicente vs {selectedMatch.opponent_name}</p>
              </div>
              <button 
                onClick={() => setSelectedMatch(null)}
                className="text-white hover:bg-white hover:bg-opacity-20 rounded-lg p-2 transition-colors"
              >
                <X size={24} />
              </button>
            </div>

            <div className="p-6 space-y-6 max-h-[80vh] overflow-y-auto">
              {loadingAnalysis && (
                <div className="text-center py-12">
                  <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto"></div>
                  <p className="mt-4 text-gray-600">Analyzing tactical data...</p>
                </div>
              )}

              {analysis && !loadingAnalysis && (
                <div className="space-y-6">
                  {/* Formation Recommendation */}
                  <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg p-6">
                    <h4 className="text-xl font-bold mb-3 flex items-center gap-2">
                      <Users size={24} />
                      Formation Recommendation
                    </h4>
                    <p className="text-lg font-semibold">{analysis.tactical_game_plan.formation_recommendation}</p>
                  </div>

                  {/* Defensive Vulnerabilities */}
                  <div className="bg-red-50 rounded-lg p-6 border-l-4 border-red-500">
                    <h4 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                      <AlertTriangle className="text-red-600" />
                      Opponent Defensive Vulnerabilities
                    </h4>
                    <div className="space-y-3">
                      {analysis.defensive_vulnerabilities.vulnerabilities.map((vuln, idx) => (
                        <div key={idx} className="bg-white rounded-lg p-4 shadow-sm">
                          <div className="flex items-start justify-between mb-2">
                            <span className="font-bold text-gray-900">{vuln.zone}</span>
                            <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                              vuln.severity === 'CRITICAL' ? 'bg-red-600 text-white' :
                              vuln.severity === 'HIGH' ? 'bg-orange-500 text-white' :
                              'bg-yellow-500 text-white'
                            }`}>
                              {vuln.severity}
                            </span>
                          </div>
                          <p className="text-sm text-gray-700 mb-2">{vuln.detail}</p>
                          <p className="text-sm text-blue-700 font-semibold">💡 {vuln.coaching_tip}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Game Phases Tactical Plan */}
                  <div className="bg-white rounded-lg p-6 shadow-md border-2 border-blue-200">
                    <h4 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                      <Clock className="text-blue-600" />
                      Game Phases Tactical Plan
                    </h4>
                    <div className="space-y-3">
                      <div className="bg-blue-50 p-4 rounded-lg">
                        <p className="font-bold text-blue-900 mb-1">0-15 min: Opening Phase</p>
                        <p className="text-sm text-gray-700">{analysis.tactical_game_plan.game_phases.first_15min}</p>
                      </div>
                      <div className="bg-blue-50 p-4 rounded-lg">
                        <p className="font-bold text-blue-900 mb-1">15-45 min: First Half Build-up</p>
                        <p className="text-sm text-gray-700">{analysis.tactical_game_plan.game_phases.minutes_15_45}</p>
                      </div>
                      <div className="bg-yellow-50 p-4 rounded-lg border-2 border-yellow-400">
                        <p className="font-bold text-yellow-900 mb-1">⏸️ Half-Time Adjustments</p>
                        <p className="text-sm text-gray-700">{analysis.tactical_game_plan.game_phases.half_time_adjustments}</p>
                      </div>
                      <div className="bg-green-50 p-4 rounded-lg">
                        <p className="font-bold text-green-900 mb-1">45-75 min: Second Half Execution</p>
                        <p className="text-sm text-gray-700">{analysis.tactical_game_plan.game_phases.minutes_45_75}</p>
                      </div>
                      <div className="bg-red-50 p-4 rounded-lg border-2 border-red-400">
                        <p className="font-bold text-red-900 mb-1">🔥 75-90 min: Final Push</p>
                        <p className="text-sm text-gray-700">{analysis.tactical_game_plan.game_phases.final_15min}</p>
                      </div>
                    </div>
                  </div>

                  {/* Player Instructions */}
                  <div className="bg-white rounded-lg p-6 shadow-md">
                    <h4 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                      <Zap className="text-yellow-500" />
                      Key Player Instructions
                    </h4>
                    <ul className="space-y-2">
                      {analysis.tactical_game_plan.key_tactical_points.map((point, idx) => (
                        <li key={idx} className="flex items-start gap-3 bg-yellow-50 p-3 rounded-lg">
                          <span className="text-yellow-600 font-bold shrink-0">▶</span>
                          <span className="text-gray-800">{point}</span>
                        </li>
                      ))}
                      {analysis.tactical_game_plan.player_instructions.map((instruction, idx) => (
                        <li key={idx} className="flex items-start gap-3 bg-blue-50 p-3 rounded-lg">
                          <span className="text-blue-600 font-bold shrink-0">•</span>
                          <span className="text-gray-800">{instruction}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Set Piece Strategy */}
                  <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-6 border-l-4 border-green-500">
                    <h4 className="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
                      <Shield className="text-green-600" />
                      Set Piece Strategy
                    </h4>
                    <p className="text-gray-800">{analysis.tactical_game_plan.set_piece_strategy}</p>
                  </div>

                  {/* Form Comparison */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-blue-50 rounded-lg p-4 border-2 border-blue-200">
                      <h5 className="font-bold text-blue-900 mb-2">Gil Vicente Form</h5>
                      <p className="text-3xl font-bold text-blue-600">{analysis.gil_vicente_form.form_string}</p>
                      <div className="mt-2 text-sm text-gray-700">
                        <p>Goals: {analysis.gil_vicente_form.goals_scored} scored, {analysis.gil_vicente_form.goals_conceded} conceded</p>
                        <p>Clean sheets: {analysis.gil_vicente_form.clean_sheets}/5</p>
                      </div>
                    </div>
                    <div className="bg-red-50 rounded-lg p-4 border-2 border-red-200">
                      <h5 className="font-bold text-red-900 mb-2">{selectedMatch.opponent_name} Form</h5>
                      <p className="text-3xl font-bold text-red-600">{analysis.opponent_form.form_string}</p>
                      <div className="mt-2 text-sm text-gray-700">
                        <p>Goals: {analysis.opponent_form.goals_scored} scored, {analysis.opponent_form.goals_conceded} conceded</p>
                        <p>Clean sheets: {analysis.opponent_form.clean_sheets}/5</p>
                        <p className="font-semibold text-red-700">Avg conceded: {analysis.opponent_form.avg_goals_conceded}/game</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Fixtures
