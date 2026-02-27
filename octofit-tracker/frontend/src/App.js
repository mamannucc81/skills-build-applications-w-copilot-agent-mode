

import './App.css';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import logo from './octofitapp-small.png';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';
import React from 'react';


function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
          <div className="container-fluid">
            <NavLink className="navbar-brand fw-bold d-flex align-items-center" to="/">
              <img src={logo} alt="OctoFit Logo" className="App-logo me-2" />
              OctoFit Tracker
            </NavLink>
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav">
                <li className="nav-item">
                  <NavLink className={({isActive}) => 'nav-link' + (isActive ? ' active' : '')} to="/activities">Actividades</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className={({isActive}) => 'nav-link' + (isActive ? ' active' : '')} to="/leaderboard">Leaderboard</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className={({isActive}) => 'nav-link' + (isActive ? ' active' : '')} to="/teams">Equipos</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className={({isActive}) => 'nav-link' + (isActive ? ' active' : '')} to="/users">Usuarios</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className={({isActive}) => 'nav-link' + (isActive ? ' active' : '')} to="/workouts">Entrenamientos</NavLink>
                </li>
              </ul>
            </div>
          </div>
        </nav>
        <div className="container">
          <Routes>
            <Route path="/" element={<Activities />} />
            <Route path="/activities" element={<Activities />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/users" element={<Users />} />
            <Route path="/workouts" element={<Workouts />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
