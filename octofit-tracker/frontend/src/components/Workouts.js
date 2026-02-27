import React, { useEffect, useState } from 'react';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const apiUrl = codespace
    ? `https://${codespace}-8000.app.github.dev/api/workouts/`
    : 'http://localhost:8000/api/workouts/';

  useEffect(() => {
    fetch(apiUrl)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setWorkouts(results);
        console.log('API endpoint:', apiUrl);
        console.log('Fetched workouts:', results);
      })
      .catch(err => console.error('Error fetching workouts:', err));
  }, [apiUrl]);

  return (
    <div>
      <h2 className="mb-4 display-6">Entrenamientos</h2>
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <table className="table table-striped table-hover">
            <thead className="table-danger">
              <tr>
                <th>#</th>
                <th>Nombre</th>
                <th>Tipo</th>
                <th>Dificultad</th>
                <th>Duración</th>
              </tr>
            </thead>
            <tbody>
              {workouts.length === 0 ? (
                <tr><td colSpan="5" className="text-center">No hay entrenamientos sugeridos.</td></tr>
              ) : (
                workouts.map((workout, idx) => (
                  <tr key={workout.id || idx}>
                    <td>{idx + 1}</td>
                    <td>{workout.name || '-'}</td>
                    <td>{workout.type || '-'}</td>
                    <td>{workout.difficulty || '-'}</td>
                    <td>{workout.duration || '-'}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
          <button className="btn btn-danger mt-2">Agregar Entrenamiento</button>
        </div>
      </div>
    </div>
  );
};

export default Workouts;
