export const exportFixtureAnalysis = (selectedMatch, statistics, tacticalPlan, format) => {
  if (!selectedMatch || !statistics || !tacticalPlan) return

  const exportData = {
    match: {
      opponent: selectedMatch.opponent_name,
      date: selectedMatch.date,
      venue: selectedMatch.is_gil_home ? 'Home' : 'Away',
      competition: selectedMatch.competition
    },
    statistics: statistics,
    tacticalPlan: tacticalPlan,
    exportDate: new Date().toISOString()
  }

  if (format === 'json') {
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${selectedMatch.opponent_name.replace(/\s+/g, '_')}_analysis_${new Date().toISOString().split('T')[0]}.json`
    a.click()
    URL.revokeObjectURL(url)
  } else if (format === 'text') {
    let txt = 'TACTICAL ANALYSIS REPORT\n'
    txt += '='.repeat(50) + '\n\n'
    txt += `Match: Gil Vicente FC vs ${selectedMatch.opponent_name}\n`
    txt += `Date: ${new Date(selectedMatch.date).toLocaleDateString('pt-PT')}\n`
    txt += `Venue: ${selectedMatch.is_gil_home ? 'Home (Estádio Cidade de Barcelos)' : 'Away'}\n`
    txt += `Competition: ${selectedMatch.competition}\n\n`
    
    if (statistics) {
      txt += 'OPPONENT STATISTICS\n' + '-'.repeat(50) + '\n'
      txt += `Team: ${statistics.team_name}\n`
      txt += `Formation: ${statistics.formation || 'N/A'}\n`
      txt += `Style: ${statistics.playing_style || 'N/A'}\n\n`
      
      if (statistics.last_match) {
        txt += 'Last Match Performance:\n'
        txt += `  Result: ${statistics.last_match.result}\n`
        txt += `  Score: ${statistics.last_match.score}\n`
        txt += `  Goals: ${statistics.last_match.goals_scored}-${statistics.last_match.goals_conceded}\n`
        txt += `  Possession: ${statistics.last_match.possession}%\n`
        txt += `  Shots: ${statistics.last_match.shots} (${statistics.last_match.shots_on_target} on target)\n\n`
      }
      
      if (statistics.strengths?.length > 0) {
        txt += 'Strengths:\n'
        statistics.strengths.forEach(s => txt += `  • ${s}\n`)
        txt += '\n'
      }
      
      if (statistics.weaknesses?.length > 0) {
        txt += 'Weaknesses:\n'
        statistics.weaknesses.forEach(w => txt += `  • ${w}\n`)
        txt += '\n'
      }
    }
    
    if (tacticalPlan) {
      txt += 'TACTICAL PLAN\n' + '-'.repeat(50) + '\n'
      txt += `Recommended Formation: ${tacticalPlan.recommended_formation || 'N/A'}\n\n`
      
      if (tacticalPlan.key_recommendations?.length > 0) {
        txt += 'Key Recommendations:\n'
        tacticalPlan.key_recommendations.forEach((rec, i) => {
          txt += `  ${i + 1}. ${rec}\n`
        })
        txt += '\n'
      }
      
      if (tacticalPlan.defensive_approach) {
        txt += `Defensive Approach:\n  ${tacticalPlan.defensive_approach}\n\n`
      }
      
      if (tacticalPlan.attacking_approach) {
        txt += `Attacking Approach:\n  ${tacticalPlan.attacking_approach}\n\n`
      }
      
      if (tacticalPlan.set_pieces) {
        txt += `Set Pieces:\n  ${tacticalPlan.set_pieces}\n\n`
      }
    }
    
    txt += '\n' + '-'.repeat(50) + '\n'
    txt += `Report generated: ${new Date().toLocaleString('pt-PT')}\n`
    txt += 'Gil Vicente FC Tactical Intelligence Platform\n'

    const blob = new Blob([txt], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${selectedMatch.opponent_name.replace(/\s+/g, '_')}_analysis_${new Date().toISOString().split('T')[0]}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }
}

export const exportOpponentAnalysis = (opponentName, tacticalData, formData, advancedStats, format) => {
  if (!opponentName) return

  const exportData = {
    opponent: opponentName,
    tacticalProfile: tacticalData,
    recentForm: formData,
    advancedStatistics: advancedStats,
    exportDate: new Date().toISOString()
  }

  if (format === 'json') {
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${opponentName.replace(/\s+/g, '_')}_opponent_analysis_${new Date().toISOString().split('T')[0]}.json`
    a.click()
    URL.revokeObjectURL(url)
  } else if (format === 'text') {
    let txt = 'OPPONENT ANALYSIS REPORT\n'
    txt += '='.repeat(50) + '\n\n'
    txt += `Team: ${opponentName}\n`
    txt += `Analysis Date: ${new Date().toLocaleDateString('pt-PT')}\n\n`
    
    if (tacticalData) {
      txt += 'TACTICAL PROFILE\n' + '-'.repeat(50) + '\n'
      txt += `Formation: ${tacticalData.formation || 'N/A'}\n`
      txt += `Playing Style: ${tacticalData.playing_style || 'N/A'}\n`
      txt += `Possession: ${tacticalData.avg_possession || 'N/A'}%\n`
      txt += `Goals per Game: ${tacticalData.avg_goals || 'N/A'}\n\n`
      
      if (tacticalData.strengths?.length > 0) {
        txt += 'Strengths:\n'
        tacticalData.strengths.forEach(s => txt += `  • ${s}\n`)
        txt += '\n'
      }
      
      if (tacticalData.weaknesses?.length > 0) {
        txt += 'Weaknesses:\n'
        tacticalData.weaknesses.forEach(w => txt += `  • ${w}\n`)
        txt += '\n'
      }
    }
    
    if (formData?.recent_matches?.length > 0) {
      txt += 'RECENT FORM\n' + '-'.repeat(50) + '\n'
      formData.recent_matches.forEach((match, i) => {
        txt += `Match ${i + 1}: ${match.result} (${match.goals_scored}-${match.goals_conceded})\n`
      })
      txt += '\n'
    }
    
    if (advancedStats) {
      txt += 'ADVANCED STATISTICS\n' + '-'.repeat(50) + '\n'
      txt += JSON.stringify(advancedStats, null, 2) + '\n\n'
    }
    
    txt += '\n' + '-'.repeat(50) + '\n'
    txt += `Report generated: ${new Date().toLocaleString('pt-PT')}\n`
    txt += 'Gil Vicente FC Tactical Intelligence Platform\n'

    const blob = new Blob([txt], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${opponentName.replace(/\s+/g, '_')}_opponent_analysis_${new Date().toISOString().split('T')[0]}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }
}

export const exportToJSON = (data, filename) => {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${filename}.json`
  a.click()
  URL.revokeObjectURL(url)
}

export const exportToText = (data, filename) => {
  let txt = 'TACTICAL ANALYSIS REPORT\n'
  txt += '='.repeat(60) + '\n\n'
  txt += `Opponent: ${data.opponent}\n`
  txt += `Generated: ${new Date().toLocaleString('pt-PT')}\n\n`
  
  if (data.statistics) {
    txt += 'STATISTICS\n' + '-'.repeat(60) + '\n'
    txt += JSON.stringify(data.statistics, null, 2) + '\n\n'
  }
  
  if (data.tacticalPlan) {
    txt += 'TACTICAL PLAN\n' + '-'.repeat(60) + '\n'
    if (data.tacticalPlan.recommended_formation) {
      txt += `Recommended Formation: ${data.tacticalPlan.recommended_formation}\n\n`
    }
    if (data.tacticalPlan.key_recommendations) {
      txt += 'Key Recommendations:\n'
      data.tacticalPlan.key_recommendations.forEach((rec, i) => {
        txt += `  ${i + 1}. ${rec}\n`
      })
      txt += '\n'
    }
    if (data.tacticalPlan.defensive_approach) {
      txt += `Defensive Approach:\n  ${data.tacticalPlan.defensive_approach}\n\n`
    }
    if (data.tacticalPlan.attacking_approach) {
      txt += `Attacking Approach:\n  ${data.tacticalPlan.attacking_approach}\n\n`
    }
  }
  
  if (data.recentMatches && data.recentMatches.length > 0) {
    txt += 'RECENT MATCHES\n' + '-'.repeat(60) + '\n'
    data.recentMatches.forEach((match, i) => {
      txt += `Match ${i + 1}: ${match.result || 'N/A'} - ${match.score || 'N/A'}\n`
    })
    txt += '\n'
  }
  
  txt += '\n' + '='.repeat(60) + '\n'
  txt += 'Gil Vicente FC - Tactical Intelligence Platform\n'

  const blob = new Blob([txt], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${filename}.txt`
  a.click()
  URL.revokeObjectURL(url)
}
