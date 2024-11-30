import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./css/langingPage.css"; 

export default function LandingPage(): JSX.Element {
  const [currentTime, setCurrentTime] = useState<Date | null>(null);
  const [error, setError] = useState<string>("");
  const [volume, setVolume] = useState<number>(1); 
  const [popupMessage, setPopupMessage] = useState<string | null>(null); 
  const audioRef = useRef<HTMLAudioElement | null>(null); 

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      setCurrentTime(now);
    }, 1000);

    return () => clearInterval(interval); 
  }, []);

  // Fetch Test Function
  function FetchTest() {
    axios
      .get("http://127.0.0.1:3000/users")
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error(error);
        setError("Failed to fetch data. Please try again later.");
      });
  }

  const handleVolumeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newVolume = parseFloat(event.target.value);
    setVolume(newVolume);

    if (audioRef.current) {
      audioRef.current.volume = newVolume; 
    }
  };

  const handlePopup = (message: string) => {
    setPopupMessage(message);
    setTimeout(() => setPopupMessage(null), 2000); 
  };

  const date = currentTime ? currentTime.toLocaleDateString() : "";
  const time = currentTime ? currentTime.toLocaleTimeString() : "";

  return (
    <div className="landing-page">
      {/* Music */}
      <audio ref={audioRef} autoPlay loop>
        <source src="src/pages/sounds/titanium-170190.mp3" type="audio/mp3" />
        Your browser does not support the audio element.
      </audio>

      {/* Popup */}
      {popupMessage && <div className="popup">{popupMessage}</div>}

      {/* Header */}
      <header className="header">
        <h1 className="title">THE MOST WANTED</h1>
        <div className="stars">
          {[...Array(5)].map((_, index) => (
            <span key={index} className="star">
              ★
            </span>
          ))}
        </div>
      </header>

      {/* Profile Icon FOR FUTURE LOGIN */}
      <div
        className="profile-icon"
        onClick={() => handlePopup("Login functionality coming soon!")}
      >
        <img src="src/pages/images/profile.png" alt="Profile" />
      </div>

      {/* Car Image */}
      <div className="car-image">
        <img src="src/pages/images/MainImage.png" alt="Car" />
      </div>

      {/* Buttons */}
      <div className="buttons">
        <button onClick={FetchTest} className="btn">
          Start Quiz ▶
        </button>
        <button
          className="btn"
          onClick={() => handlePopup("Coming soon in future updates")}
        >
          Leader Board
        </button>
        <button
          className="btn"
          onClick={() => handlePopup("Coming soon in future updates")}
        >
          Multiplayer
        </button>
        <button
          className="btn"
          onClick={() => handlePopup("Coming soon in future updates")}
        >
          Settings
        </button>
      </div>

      {/* Volume Control */}
      <div className="volume-control">
        <label htmlFor="volume-slider">Volume: </label>
        <input
          id="volume-slider"
          type="range"
          min="0"
          max="1"
          step="0.01"
          value={volume}
          onChange={handleVolumeChange}
        />
      </div>

      {/* TIMER AND DATE */}
      <footer className="footer">
        {error && <div className="error">{error}</div>}
        <div className="timer">
          <div className="date-box">{date}</div>
          <div className="time-box">{time}</div>
        </div>
      </footer>
    </div>
  );
}
