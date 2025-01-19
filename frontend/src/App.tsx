import { useState } from "react";
import Hero from "./components/Hero";


function App() {
  const [count, setCount] = useState(0);
  const [isNightMode, setIsNightMode] = useState(true);
  const toggleMode = () => setIsNightMode(!isNightMode);


  return (
    <div
      className={`w-full h-screen ${
        isNightMode ? "bg-customBlack text-white" : "bg-[#F7F7F7] text-black"
      }`}
    >
      <button
        onClick={toggleMode}
        className="absolute top-4 right-4 px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-500 transition"
      >
        {isNightMode ? "Switch to Light Mode" : "Switch to Night Mode"}
      </button>
      <Hero />
    </div>
  );
}

export default App;
