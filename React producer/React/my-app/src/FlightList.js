import React, { useState, useEffect } from 'react';
import { PlaneTakeoff, Edit2, Trash2 } from 'lucide-react';

const FlightsManager = () => {
    const [flights, setFlights] = useState([]);
    const [flight, setFlight] = useState({ id: '', flight_id: '', status: '', gate: '' });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Define fetchFlights function
    const fetchFlights = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/flights');
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            setFlights(data);
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFlights();
    }, []);

    const handleAddFlight = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/flights', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    flight_id: flight.flight_id,
                    status: flight.status,
                    gate: flight.gate,
                }),
            });
            if (!response.ok) throw new Error('Network response was not ok');
            await response.json();
            // Refresh the flight list after adding
            await fetchFlights();
        } catch (error) {
            setError(error.message);
        }
    };

    const handleEditFlight = async (id) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/flights/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    flight_id: flight.flight_id,
                    status: flight.status,
                    gate: flight.gate,
                }),
            });
            if (!response.ok) throw new Error('Network response was not ok');
            await response.json();
            // Refresh the flight list after editing
            await fetchFlights();
        } catch (error) {
            setError(error.message);
        }
    };

    const handleDeleteFlight = async (id) => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/flights/${id}`, {
                method: 'DELETE',
            });
            if (!response.ok) throw new Error('Network response was not ok');
            await response.json();
            // Refresh the flight list after deleting
            await fetchFlights();
        } catch (error) {
            setError(error.message);
        }
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <>
      <nav class="navbar navbar-expand-lg">
  <div class="container-fluid">
    
    <a class="navbar-brand mx-auto" href="#">
      <img src="https://seekvectorlogo.com/wp-content/uploads/2022/01/indigo-vector-logo-2022-small.png" alt="Bootstrap" width="160" height="120"/>
    </a>
    
  
      
    </div>
  
</nav>
        <div className="airline-bg">
          <div className="container-fluid">
            <div className="row justify-content-center">
              <div className="col-md-8">
                <div className="card shadow-lg">
                  <div className="card-body">
                    <h1 className="card-title text-center mb-4">
                      <PlaneTakeoff className="me-2" size={40} />
                      Flight Management
                    </h1>
                    <form>
                      <div className="mb-3">
                        <input
                          type="text"
                          className="form-control"
                          placeholder="Flight ID"
                          value={flight.flight_id}
                          onChange={(e) => setFlight({ ...flight, flight_id: e.target.value })}
                        />
                      </div>
                      <div className="mb-3">
                        <input
                          type="text"
                          className="form-control"
                          placeholder="Status"
                          value={flight.status}
                          onChange={(e) => setFlight({ ...flight, status: e.target.value })}
                        />
                      </div>
                      <div className="mb-3">
                        <input
                          type="text"
                          className="form-control"
                          placeholder="Gate"
                          value={flight.gate}
                          onChange={(e) => setFlight({ ...flight, gate: e.target.value })}
                        />
                      </div>
                      <button className="btn btn-primary w-100" onClick={handleAddFlight}>
                        Add Flight
                      </button>
                    </form>
                    <hr className="my-4" />
                    <h2 className="h4 mb-3">Flight List</h2>
                    <ul className="list-group">
                      {flights.map((f) => (
                        <li key={f.id} className="list-group-item d-flex justify-content-between align-items-center">
                          <div>
                            <strong>ID: {f.flight_id}</strong>
                            <br />
                            Status: {f.status}, Gate: {f.gate}
                          </div>
                          <div>
                            <button className="btn btn-outline-primary btn-sm me-2" onClick={() => handleEditFlight(f.id)}>
                              <Edit2 size={16} />
                            </button>
                            <button className="btn btn-outline-danger btn-sm" onClick={() => handleDeleteFlight(f.id)}>
                              <Trash2 size={16} />
                            </button>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        </>
      );
    };
export default FlightsManager;
