
import React, { useEffect, useState } from 'react';
const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const apiUrl = codespace
    ? `https://${codespace}-8000.app.github.dev/api/leaderboard/`
    : 'http://localhost:8000/api/leaderboard/';

  useEffect(() => {
    fetch(apiUrl)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setLeaderboard(results);
        console.log('API endpoint:', apiUrl);
        console.log('Fetched leaderboard:', results);
      })
      .catch(err => console.error('Error fetching leaderboard:', err));
  }, [apiUrl]);

  return (
    <div>
      <h2 className="mb-4 display-6">Leaderboard</h2>
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <table className="table table-striped table-hover">
            <thead className="table-success">
              <tr>
                <th>#</th>
                <th>Usuario</th>
                <th>Puntos</th>
                <th>Equipo</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.length === 0 ? (
                <tr><td colSpan="4" className="text-center">No hay datos de leaderboard.</td></tr>
              ) : (
                leaderboard.map((entry, idx) => (
                  <tr key={entry.id || idx}>
                    <td>{idx + 1}</td>
                    <td>{entry.username || entry.name || '-'}</td>
                    <td>{entry.points || entry.score || '-'}</td>
                    <td>{entry.team || entry.team_name || '-'}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
          <button className="btn btn-success mt-2">Actualizar Leaderboard</button>
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;
