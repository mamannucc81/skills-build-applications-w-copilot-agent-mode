import React, { useEffect, useState } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const apiUrl = codespace
    ? `https://${codespace}-8000.app.github.dev/api/activities/`
    : 'http://localhost:8000/api/activities/';

  useEffect(() => {
    fetch(apiUrl)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setActivities(results);
        console.log('API endpoint:', apiUrl);
        console.log('Fetched activities:', results);
      })
      .catch(err => console.error('Error fetching activities:', err));
  }, [apiUrl]);

  return (
    <div>
      <h2 className="mb-4 display-6">Actividades</h2>
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <table className="table table-striped table-hover">
            <thead className="table-primary">
              <tr>
                <th>#</th>
                <th>Nombre</th>
                <th>Tipo</th>
                <th>Duración</th>
                <th>Fecha</th>
              </tr>
            </thead>
            <tbody>
              {activities.length === 0 ? (
                <tr><td colSpan="5" className="text-center">No hay actividades registradas.</td></tr>
              ) : (
                activities.map((act, idx) => (
                  <tr key={act.id || idx}>
                    <td>{idx + 1}</td>
                    <td>{act.name || act.title || '-'}</td>
                    <td>{act.type || '-'}</td>
                    <td>{act.duration || '-'}</td>
                    <td>{act.date || act.created_at || '-'}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
          <button className="btn btn-primary mt-2">Agregar Actividad</button>
        </div>
      </div>
    </div>
  );
};

export default Activities;
