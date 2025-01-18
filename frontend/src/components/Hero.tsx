import { useState, useEffect } from "react";
import Trending from "../components/Trending";
import WebCritique from "./WebCritique";

const options = [
  { value: "www.youtube.com", label: "ww.youtube.com" },
  { value: "www.apple.com", label: "ww.apple.com" },
  { value: "www.meta.com", label: "ww.meta.com" },
];

const Hero = () => {
  const [query, setQuery] = useState<string>(""); // Track user input
  const [results, setResults] = useState<string[]>([]); // Track API results
  const [loading, setLoading] = useState<boolean>(false); // Loading state

  // Debounced function to fetch results from the backend
  useEffect(() => {
    const fetchResults = async () => {
      if (query.length < 2) {
        setResults([]);
        return;
      }
      setLoading(true);
      try {
        const response = await fetch(
          `/api/search?query=${encodeURIComponent(query)}`
        );
        const data = await response.json();
        setResults(data.results); // Update with backend results
      } catch (error) {
        console.error("Error fetching results:", error);
        setResults([]);
      } finally {
        setLoading(false);
      }
    };

    // Add debounce logic
    const debounce = setTimeout(fetchResults, 300); // Wait 300ms after user stops typing
    return () => clearTimeout(debounce); // Clear timeout on cleanup or input change
  }, [query]);

  return (
    <div className="w-full h-screen flex  bg-gradient-to-r from-gray-700 to-gray-950 items-center ">
      <div className=" w-[50%] h-[50%] flex flex-col justify-center items-center">
        <h1 className="m-auto text-red-700 text-[50px] font-sans font-[900]">
          Kritique✍️
        </h1>

        <p className="m-auto font-[400] text-[20px] text-white">
          Enter a company you'd like to{" "}
          <span className="text-red-700">Kritique!</span>
        </p>

        {/* <Select
          className="m-auto w-[400px] border-spacing-[10px] border-red-700"
          options={options}
          isClearable
          placeholder="Search or type custom input..."
          onChange={handleChange}
        /> */}

        <input
          className="m-auto w-[400px] border-spacing-[10px] border-red-700"
          type="text"
          placeholder="Search for a company..."
          value={query}
          onChange={(e) => setQuery(e.target.value)} // Update query on input change
        />

        {/* Results */}
        <div className="mt-4 w-[400px] bg-white rounded-md shadow-md">
          {loading ? (
            <div className="p-4 text-gray-500">Loading...</div>
          ) : results.length > 0 ? (
            <ul>
              {results.map((result, index) => (
                <li
                  key={index}
                  className="px-4 py-2 border-b last:border-b-0 hover:bg-gray-100 cursor-pointer"
                  onClick={() => setQuery(result)} // Allow user to select a result
                >
                  {result}
                </li>
              ))}
            </ul>
          ) : (
            <div className="p-4 text-gray-500">No matches</div>
          )}
        </div>

        <button
          className="text-white bg-red-700 rounded-md p-2 m-auto"
          onClick={() => console.log("Search for:", query)} // Add your search action here
        >
          Search
        </button>
      </div>

      <Trending />

      {/* <WebCritique /> */}
    </div>
  );
};

export default Hero;
