import React from "react";

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

  return (
    <div id="review" className="h-full  py-10">
      <h1 className="m-2 text-red-500 text-[50px] font-sans font-[900] border-b-4">
        {domain}
      </h1>

      <div className="mb-16 flex flex-col m-auto justify-between w-full h-full">
          <div className="flex flex-row text-center rounded-md p-2 h-full">
            <div className="h-full">
              <p className="h-full py-0 px-2 bg-gray-600 text-red-500 text-[50px] font-[700] rounded-md mx-2">
                {rating.toFixed(1)}
              </p>
            </div>
            <div>
              <p className="h-full min-h-full py-auto px-2 bg-gray-600 text-white text-[15px] font-[700] rounded-md mx-2">
                AI Review:{aiSummary}
              </p>
            </div>
          </div>

          <div className="flex flex-col w-90 mx-4 text-center bg-gray-600 items-start rounded-md mt-1 pt-1 pb-2 px-2">
            <p className="text-white font-[600]">Tags:</p>
            <div className="flex flex-row flex-wrap text-sm items-start">
              {tags.map((tag, index) => (
                <p className="bg-white m-2 p-2 rounded-xl" key={index}>
                  {tag}
                </p>
              ))}
            </div>
          </div>
      </div>

      <h3 className="m-2 p-2 rounded-md text-red-700 bg-gray-600 text-[20px]">
        Critiques
      </h3>

      <ul className="m-2 text-red-700 bg-gray-600 text-[20px] font-[700] p-2 rounded-md">
        {comments.map((comment, index) => (
          <li key={index}>
            {comment.time} - {comment.text || "No comment provided"}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default WebCritique;
