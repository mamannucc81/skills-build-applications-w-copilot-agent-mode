
import React, { useEffect, useState } from 'react';
const Teams = () => {
  const [teams, setTeams] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const apiUrl = codespace
    ? `https://${codespace}-8000.app.github.dev/api/teams/`
    : 'http://localhost:8000/api/teams/';

  useEffect(() => {
    fetch(apiUrl)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setTeams(results);
        console.log('API endpoint:', apiUrl);
        console.log('Fetched teams:', results);
      })
      .catch(err => console.error('Error fetching teams:', err));
  }, [apiUrl]);

  return (
    <div>
      <h2 className="mb-4 display-6">Equipos</h2>
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <table className="table table-striped table-hover">
            <thead className="table-info">
              <tr>
                <th>#</th>
                <th>Nombre</th>
                <th>Miembros</th>
                <th>Puntos</th>
              </tr>
            </thead>
            <tbody>
              {teams.length === 0 ? (
                <tr><td colSpan="4" className="text-center">No hay equipos registrados.</td></tr>
              ) : (
                teams.map((team, idx) => (
                  <tr key={team.id || idx}>
                    <td>{idx + 1}</td>
                    <td>{team.name || '-'}</td>
                    <td>{team.members ? team.members.length : '-'}</td>
                    <td>{team.points || team.score || '-'}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
          <button className="btn btn-info mt-2">Crear Equipo</button>
        </div>
      </div>
    </div>
  );
};

export default Teams;
