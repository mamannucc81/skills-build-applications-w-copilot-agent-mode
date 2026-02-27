import React, { useEffect, useState } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const apiUrl = codespace
    ? `https://${codespace}-8000.app.github.dev/api/users/`
    : 'http://localhost:8000/api/users/';

  useEffect(() => {
    fetch(apiUrl)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setUsers(results);
        console.log('API endpoint:', apiUrl);
        console.log('Fetched users:', results);
      })
      .catch(err => console.error('Error fetching users:', err));
  }, [apiUrl]);

  return (
    <div>
      <h2 className="mb-4 display-6">Usuarios</h2>
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <table className="table table-striped table-hover">
            <thead className="table-warning">
              <tr>
                <th>#</th>
                <th>Usuario</th>
                <th>Email</th>
                <th>Equipo</th>
              </tr>
            </thead>
            <tbody>
              {users.length === 0 ? (
                <tr><td colSpan="4" className="text-center">No hay usuarios registrados.</td></tr>
              ) : (
                users.map((user, idx) => (
                  <tr key={user.id || idx}>
                    <td>{idx + 1}</td>
                    <td>{user.username || user.name || '-'}</td>
                    <td>{user.email || '-'}</td>
                    <td>{user.team || user.team_name || '-'}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
          <button className="btn btn-warning mt-2">Agregar Usuario</button>
        </div>
      </div>
    </div>
  );
};

export default Users;
