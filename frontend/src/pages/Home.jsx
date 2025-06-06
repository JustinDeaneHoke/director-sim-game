import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/api';

const Home = () => {
  const [name, setName] = useState('');
  const navigate = useNavigate();

  const startGame = async (e) => {
    e.preventDefault();
    try {
      await api.post('/start_game', { directorName: name });
      navigate('/dashboard');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form onSubmit={startGame} className="bg-white p-6 rounded shadow-md space-y-4">
        <h1 className="text-2xl font-bold">Start Your Directing Career</h1>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Director Name"
          className="border rounded w-full p-2"
          required
        />
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
        >
          Start My Directing Career
        </button>
      </form>
    </div>
  );
};

export default Home;
