import React, { useState } from "react";
const url = "https://kritique.vercel.app";

interface Comment {
  rating: number;
  text: string;
  time: string;
}

interface WebCritiqueProps {
  data: {
    aiSummary: string;
    comments: Comment[];
    domain: string;
    rating: number;
    tags: string[];
  };
}

const WebCritique: React.FC<WebCritiqueProps> = ({ data }) => {
  const { aiSummary, comments, domain, rating, tags } = data;

  const [newComment, setNewComment] = useState<string>("");
  const [newRating, setNewRating] = useState<number>(5); // Default rating
  const [error, setError] = useState<string | null>(null);

  const handlePostCritique = async () => {
    if (!newComment.trim()) {
      setError("Comment cannot be empty");
      return;
    }

    setError(null); // Clear any existing error

    const critiqueData = {
      website: domain,
      critique: newComment,
      rating: newRating,
    };

    try {
      const response = await fetch(`${url}/post_critique`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(critiqueData),
      });

      const result = await response.json();

      if (result.success) {
        alert("Critique posted successfully!");

        // Optionally, you could refresh the comments by refetching data
        // Or append the new comment locally to `comments`
      } else {
        setError("Failed to post critique. Please try again.");
      }
    } catch (error) {
      console.error("Error posting critique:", error);
      setError("An unexpected error occurred. Please try again.");
    }
  };

  const matteColors = [
    'bg-blue-200',  // Soft blue
    'bg-green-200', // Soft green
    'bg-red-200',   // Soft red
    'bg-yellow-200',// Soft yellow
    'bg-purple-200',// Soft purple
    'bg-slate-300'  // Soft slate
  ];
  // shuffle matte colors

  const textColor = rating < 2 ? 'text-red-500' : rating < 4 ? 'text-orange-500' : 'text-green-500';

  return (
    <div id="review" className="h-full  py-10">
      <h1 className={`m-2 ${textColor} text-[50px] font-sans font-[900] border-b-4`}>
        {domain}
      </h1>

      <div className="mb-16 flex flex-col m-auto justify-between w-full h-max">
          <div className="flex flex-row text-center rounded-md p-2 h-30">
            <div className="flex items-center">
              <p
                className={`h-full py-0 px-2 bg-gray-600 text-[50px] font-[700] rounded-md mx-2 ${
                  rating === 0 ? 'text-gray-500' : textColor
                }`}
              >
                {rating===0 ? "N/A" : rating.toFixed(1)}
              </p>
            </div>
            <div className="flex items-center w-full">
              <div className="mx-2 px-1 bg-gray-600 py-auto h-full flex w-full flex-row items-center rounded-md">
                <p className="m-auto text-white text-[15px] font-[700] ">
                  AI Review: {aiSummary}
                </p>
              </div>
            </div>
          </div>

          <div className="flex flex-col w-90 mx-4 text-center bg-gray-600 items-start rounded-md mt-1 pt-1 pb-2 px-2">
            <p className="text-white font-[600]">Tags:</p>
            <div className="flex flex-row flex-wrap text-sm items-start">
              {tags.map((tag, index) => 
              {
                const colorClass = matteColors[index % matteColors.length]; // Rotate through colors
                return (
                  <p className={`m-2 p-2 rounded-xl ${colorClass}`} key={index}>
                    {tag}
                  </p>
                );
              })}
            </div>
          </div>
      </div>

      <div>
        <h3 className="m-2 p-2 rounded-md text-white bg-gray-600 text-[20px]">
          Kritiques⚡
        </h3>
        <div className="m-2 p-2 ">
          <p className="text-white">Add a new critique</p>
          <input
            type="text"
            className="rounded-md p-2 mr-2 w-full "
            placeholder="Write your critique..."
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
          />

          <input
            type="number"
            className="rounded-md p-2 mr-2"
            placeholder="Rating (1-5)"
            value={newRating}
            onChange={(e) => setNewRating(Number(e.target.value))}
            min={1}
            max={5}
          />

          <button onClick={handlePostCritique} className="text-[30px]">
            ⬆️
          </button>
          {error && <p className="text-red-500 mt-2">{error}</p>}
        </div>

        <ul className="m-2 text-white bg-gray-600 text-[20px] font-[700] p-2 rounded-md">
          {comments.map((comment, index) => (
            <li key={index} className="my-4 border-b-2 border-black">
              {new Date(comment.time).toLocaleDateString("en-US", {
                year: "numeric",
                month: "long",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
              })}{" "}
              : {comment.text || "No comment provided"} -{" "}
              {comment.rating + "💫"}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default WebCritique;
