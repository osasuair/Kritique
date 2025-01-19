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
    <div id="review" className="w-[90%]  py-10">
      <h1 className="m-2 text-red-700 text-[50px] font-sans font-[900] border-b-4">
        {domain}
      </h1>

      <div className="mb-16 flex flex-row m-auto justify-between">
        <p className="h-[50%] bg-gray-600 text-red-700 text-[50px] font-[700] p-2 rounded-md mx-2">
          {rating.toFixed(1)}
        </p>
        <p className=" h-[50%] bg-gray-600 text-red-700 text-[15px] font-[700] p-2 rounded-md mx-2">
          AI Review:{aiSummary}
        </p>
        <div className="flex flex-col w-[18%]  mx-2 text-center bg-gray-600 rounded-md p-2">
          <p className="text-white  font-[700]">Tags</p>
          <ul className=" text-red-700 text-[10px] font-[700] ">
            {tags.map((tag, index) => (
              <li className="bg-white m-2 p-2 rounded-xl" key={index}>
                {tag}
              </li>
            ))}
          </ul>
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
