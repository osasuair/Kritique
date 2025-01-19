import { useState, useEffect } from "react";
import Trending from "../components/Trending";
import WebCritique from "./WebCritique";

const url = "https://kritique.vercel.app";

// const options = [
//   { value: "www.youtube.com", label: "ww.youtube.com" },
//   { value: "www.apple.com", label: "ww.apple.com" },
//   { value: "www.meta.com", label: "ww.meta.com" },
// ];

// const data = {
//   aiSummary:
//     "Users have mixed opinions on youtube.com. Some find it visually appealing, helpful, and informative, while others cite errors, crashes, slow performance, poor navigation, and accessibility issues.",
//   comments: [
//     {
//       rating: 4,
//       text: "",
//       time: "Sat, 01 Jan 2000 05:00:00 GMT",
//     },
//     {
//       rating: 4,
//       text: "This website has a great design, but the navigation could be improved.",
//       time: "Sat, 18 Jan 2025 18:06:26 GMT",
//     },
//     {
//       rating: 4,
//       text: "This website has a great design, but the navigation could be improved.",
//       time: "Sat, 18 Jan 2025 18:06:26 GMT",
//     },
//     {
//       rating: 4,
//       text: "This website has a great design, but the navigation could be improved.",
//       time: "Sat, 18 Jan 2025 18:06:26 GMT",
//     },
//     {
//       rating: 4,
//       text: "This website has a great design, but the navigation could be improved.",
//       time: "Sat, 18 Jan 2025 18:06:26 GMT",
//     },
//     {
//       rating: 4,
//       text: "This website has a great design, but the navigation could be improved.",
//       time: "Sat, 18 Jan 2025 18:06:26 GMT",
//     },
//   ],
//   domain: "youtube.com",
//   rating: 4.3,
//   tags: [
//     "video sharing",
//     "content creation",
//     "social media",
//     "entertainment",
//     "educational resource",
//     "marketing platform",
//   ],
// };

const Hero = () => {
  const [query, setQuery] = useState<string>(""); // Track user input
  const [results, setResults] = useState<{ domain: string }[]>([]); // Track API results
  const [loading, setLoading] = useState<boolean>(false); // Loading state
  const [data, setData] = useState<any>(null); // Store the critique data
  const [adding, setAdding] = useState<boolean>(false); // Track adding process (e.g. POST request)
  const [trends, setTrends] = useState<string[]>([]); // Store the trending data

  useEffect(() => {
    //trends
    // Fetch critique data for a selected domain
    const fetchTrends = async () => {
      try {
        const response = await fetch(`${url}/get_top_10_websites`);
        const trendsData = await response.json();
        setTrends(trendsData); // Store the fetched data in the `trends` variable
        console.log("Fetched top websites:", trendsData);
      } catch (error) {
        console.error("Error fetching top websites:", error);
        setTrends([]); // Clear data in case of error
      }
    };

    fetchTrends();
  }, []);
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
          `${url}/get_search_suggestions?query=${encodeURIComponent(query)}`
        );
        const data = await response.json();
        console.log(data);
        setResults(data); // Update with backend results
        //console.log(data.results);
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

  // Fetch critique data for a selected domain
  const fetchCritique = async (website: string) => {
    try {
      const response = await fetch(
        `${url}/get_website_critique?website=${encodeURIComponent(website)}`
      );
      const critiqueData = await response.json();
      setData(critiqueData); // Store the fetched data in the `data` variable
      console.log("Fetched critique data:", critiqueData);
    } catch (error) {
      console.error("Error fetching critique data:", error);
      setData(null); // Clear data in case of error
    }
  };

  //   add a new website
  const addWebsite = async (domain: string) => {
    setAdding(true);
    try {
      const response = await fetch(`${url}/add_website`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ domain }),
      });
      const result = await response.json();
      if (result.status === "Success") {
        // Once added, fetch the critique for this domain
        await fetchCritique(domain);
      } else {
        console.error("Failed to add website:", result);
      }
    } catch (error) {
      console.error("Error adding website:", error);
    } finally {
      setAdding(false);
    }
  };

  // Scroll to the WebCritique component when data is updated
  useEffect(() => {
    if (data) {
      const critiqueElement = document.getElementById("review");
      critiqueElement?.scrollIntoView({ behavior: "smooth" }); // Smooth scroll to WebCritique section
    }
  }, [data]);

  return (
    <div className="w-full  flex-col   items-center ">
      <div className="w-full h-screen flex items-center">
        <div className=" w-[50%] h-[50%] flex flex-col justify-center items-center">
          <h1 className="m-auto text-red-700 text-[50px] font-sans font-[900]">
            Kritique✍️
          </h1>

          <p className="m-auto font-[400] text-[20px] text-white">
            Enter a company you'd like to{" "}
            <span className="text-red-700">Kritique!</span>
          </p>

          <input
            className="m-auto w-[400px] border-spacing-[10px] border-red-700 rounded-md p-1"
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
                    onClick={() => fetchCritique(result.domain)} // Fetch critique on click
                  >
                    {result.domain}
                  </li>
                ))}
              </ul>
            ) : (
              <div className="p-4 text-gray-500">No matches</div>
            )}
          </div>

          <button
            className="text-white bg-red-700 rounded-md p-2 m-auto"
            onClick={() => {
              if (results.length === 0) {
                addWebsite(query); // If no results, add website
              } else {
                console.log("Search for:", query); // Add your search action here
              }
            }}
          >
            {adding ? "Adding..." : "Search"}
          </button>
        </div>

        <Trending trends={trends} />
      </div>

      {/* Conditionally render WebCritique if data is available */}
      {data ? <WebCritique data={data[0]} /> : null}
    </div>
  );
};

export default Hero;
