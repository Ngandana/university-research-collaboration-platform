// src/pages/Dashboard.js
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getUsers, getProjects, getTasks } from '../services/api';
import { useAuth } from '../context/AuthContext';

const STATUS_BADGE = {
  ACTIVE: 'badge-green', CREATED: 'badge-blue', COMPLETED: 'badge-gray',
  CANCELLED: 'badge-red', ARCHIVED: 'badge-gray',
  ASSIGNED: 'badge-blue', IN_PROGRESS: 'badge-yellow', OVERDUE: 'badge-red',
};

export default function Dashboard() {
  const { currentUser } = useAuth();
  const [stats, setStats]       = useState({ users: 0, projects: 0, tasks: 0, overdue: 0 });
  const [projects, setProjects] = useState([]);
  const [tasks, setTasks]       = useState([]);
  const [loading, setLoading]   = useState(true);

  useEffect(() => {
    Promise.all([getUsers(), getProjects(), getTasks(), getTasks({ overdue: true })])
      .then(([u, p, t, ov]) => {
        setStats({ users: u.data.length, projects: p.data.length, tasks: t.data.length, overdue: ov.data.length });
        setProjects(p.data.slice(0, 5));
        setTasks(t.data.slice(0, 5));
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading-wrap"><div className="spinner" /></div>;

  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">{greeting}, {currentUser?.name?.split(' ')[0] || 'Researcher'} 👋</h1>
          <p className="page-subtitle">Here's what's happening on the platform today.</p>
        </div>
        <Link to="/projects" className="btn btn-primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 5v14M5 12h14"/></svg>
          New Project
        </Link>
      </div>

      <div className="stats-grid">
        {[
          { label: 'Total Users',     value: stats.users,    icon: '👥', sub: 'registered accounts',   color: 'var(--accent)' },
          { label: 'Active Projects', value: stats.projects, icon: '📁', sub: 'research projects',      color: 'var(--accent-2)' },
          { label: 'Total Tasks',     value: stats.tasks,    icon: '✅', sub: 'across all projects',    color: 'var(--success)' },
          { label: 'Overdue Tasks',   value: stats.overdue,  icon: '⚠️', sub: 'need attention',         color: 'var(--danger)' },
        ].map(s => (
          <div key={s.label} className="stat-card">
            <div className="stat-icon">{s.icon}</div>
            <div className="stat-value" style={{ color: s.color }}>{s.value}</div>
            <div className="stat-label">{s.label}</div>
            <div className="stat-sub">{s.sub}</div>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        {/* Recent Projects */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <h3 style={{ fontSize: 15 }}>Recent Projects</h3>
            <Link to="/projects" style={{ fontSize: 13, color: 'var(--accent)' }}>View all →</Link>
          </div>
          {projects.length === 0
            ? <div className="empty-state" style={{ padding: '30px 0' }}><p>No projects yet.</p></div>
            : projects.map(p => (
              <div key={p.project_id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 0', borderBottom: '1px solid var(--border)' }}>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 500 }}>{p.title}</div>
                  <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>{p.owner_name} · {p.member_count} members</div>
                </div>
                <span className={`badge ${STATUS_BADGE[p.status] || 'badge-gray'}`}>{p.status}</span>
              </div>
            ))
          }
        </div>

        {/* Recent Tasks */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <h3 style={{ fontSize: 15 }}>Recent Tasks</h3>
            <Link to="/tasks" style={{ fontSize: 13, color: 'var(--accent)' }}>View all →</Link>
          </div>
          {tasks.length === 0
            ? <div className="empty-state" style={{ padding: '30px 0' }}><p>No tasks yet.</p></div>
            : tasks.map(t => (
              <div key={t.task_id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 0', borderBottom: '1px solid var(--border)' }}>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 500 }}>{t.title}</div>
                  <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>Due {t.deadline}</div>
                </div>
                <span className={`badge ${STATUS_BADGE[t.status] || 'badge-gray'}`}>{t.status}</span>
              </div>
            ))
          }
        </div>
      </div>
    </div>
  );
}
