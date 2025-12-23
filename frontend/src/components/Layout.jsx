import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Home, Calendar, Users, TrendingUp } from 'lucide-react'

const Layout = ({ children }) => {
  const location = useLocation()
  
  const navItems = [
    { path: '/', label: 'Dashboard', icon: Home },
    { path: '/fixtures', label: 'Fixtures', icon: Calendar },
    { path: '/opponents', label: 'Opponents', icon: Users },
  ]
  
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-[#003C71] text-white shadow-lg">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <TrendingUp size={32} />
              <div>
                <h1 className="text-2xl font-bold">Gil Vicente FC</h1>
                <p className="text-sm text-gray-300">Tactical Intelligence Platform</p>
              </div>
            </div>
          </div>
        </div>
      </header>
      
      {/* Navigation */}
      <nav className="bg-white border-b shadow-sm">
        <div className="container mx-auto px-4">
          <div className="flex space-x-8">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={`flex items-center space-x-2 py-4 border-b-2 transition-colors ${
                  location.pathname === path
                    ? 'border-[#C41E3A] text-[#C41E3A]'
                    : 'border-transparent text-gray-600 hover:text-[#C41E3A]'
                }`}
              >
                <Icon size={20} />
                <span className="font-medium">{label}</span>
              </Link>
            ))}
          </div>
        </div>
      </nav>
      
      {/* Main Content */}
      <main className="flex-1 container mx-auto px-4 py-8">
        {children}
      </main>
      
      {/* Footer */}
      <footer className="bg-gray-800 text-white py-4">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm">
            © 2025 Gil Vicente Tactical Intelligence Platform - Built for Gil Vicente FC
          </p>
        </div>
      </footer>
    </div>
  )
}

export default Layout
