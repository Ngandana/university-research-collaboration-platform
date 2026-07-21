// src/components/Sidebar.js
import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Icon = ({ d }) => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
    stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d={d} />
  </svg>
);

const ICONS = {
  dashboard: "M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z",
  projects:  "M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z",
  tasks:     "M9 11l3 3L22 4 M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7",
  users:     "M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2 M23 21v-2a4 4 0 0 0-3-3.87 M16 3.13a4 4 0 0 1 0 7.75",
  logout:    "M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4 M16 17l5-5-5-5 M21 12H9",
};

export default function Sidebar() {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => { logout(); navigate('/login'); };

  const initials = currentUser?.name
    ? currentUser.name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
    : 'U';

  const BADGE_COLOR = {
    SUPERVISOR: 'badge-blue', RESEARCHER: 'badge-purple',
    STUDENT: 'badge-green', ADMIN: 'badge-yellow',
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <h2>
          <div className="logo-icon">🎓</div>
          Research Platform
        </h2>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Navigation</div>

        <NavLink to="/dashboard" className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}>
          <Icon d={ICONS.dashboard} /> Dashboard
        </NavLink>
        <NavLink to="/projects" className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}>
          <Icon d={ICONS.projects} /> Projects
        </NavLink>
        <NavLink to="/tasks" className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}>
          <Icon d={ICONS.tasks} /> Tasks
        </NavLink>
        <NavLink to="/users" className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}>
          <Icon d={ICONS.users} /> Users
        </NavLink>
      </nav>

      <div className="sidebar-footer">
        <div className="user-pill">
          <div className="avatar">{initials}</div>
          <div className="user-pill-info">
            <div className="user-pill-name">{currentUser?.name || 'Guest'}</div>
            <div className="user-pill-role">{currentUser?.role || ''}</div>
          </div>
          <button className="btn-icon" onClick={handleLogout} title="Logout">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4 M16 17l5-5-5-5 M21 12H9"/>
            </svg>
          </button>
        </div>
      </div>
    </aside>
  );
}
