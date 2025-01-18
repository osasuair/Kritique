import React from "react";

const WebCritique = () => {
  return (
    <div className="w-[90%] h-[50%] m-auto">
      <h1 className="m-2 text-red-700 text-[50px] font-sans font-[900] border-b-4">
        Site Name
      </h1>

      <div className="mb-16 flex flex-row m-auto justify-between">
        <p className=" bg-gray-600 text-red-700 text-[50px] font-[700] p-2 rounded-md">
          4.5
        </p>
        <p className="bg-gray-600 text-red-700 text-[10px] font-[700] p-2 rounded-md">
          AI Review:{" "}
        </p>
        <div>
          <ul className="bg-gray-600 text-red-700 text-[10px] font-[700] p-2 rounded-md">
            <li>tag1</li>
            <li>tag2</li>
          </ul>
        </div>
      </div>

      <h3 className="m-2 p-2 rounded-md text-red-700 bg-gray-600 text-[20px]">
        Critiques
      </h3>

      <ul className="m-2 text-red-700 bg-gray-600 text-[20px] font-[700] p-2 rounded-md">
        <li>Name Time comment</li>
      </ul>
    </div>
  );
};

export default WebCritique;
