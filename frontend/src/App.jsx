import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Opponents from './pages/Opponents'
import TacticalAnalysis from './pages/TacticalAnalysis'
import Fixtures from './pages/Fixtures'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/fixtures" element={<Fixtures />} />
        <Route path="/opponents" element={<Opponents />} />
        <Route path="/opponents/:teamId/analysis" element={<TacticalAnalysis />} />
      </Routes>
    </Layout>
  )
}

export default App
