import { Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/landingPage';
import GamePage from './pages/gamePage';
import PlayerPage from './pages/playerPage';

export default function App() {
  return (
    <>
      <Routes>
        <Route path='/' element={<LandingPage />} />

        {/* Conditional routes */}
        <Route path='player' element={<PlayerPage />} />
        <Route path='game' element={<GamePage />} />
        {/* Non-existing routes */}
        <Route path='/*' element={<Navigate to='/' />} />
      </Routes>
    </>
  );
}
