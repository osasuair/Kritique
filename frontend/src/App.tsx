import { useState } from "react";
import Hero from "./components/Hero";

function App() {
  const [count, setCount] = useState(0);

  return (

    // dark slate radial gradient to black
    <div className="w-full b" style={{background: "radial-gradient(circle, #2c3e50, #000000)"}}>
      <Hero />
    </div>
  );
}

export default App;
