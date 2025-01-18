import React from "react";
import Select from "react-select";

const options = [
  { value: "www.youtube.com", label: "ww.youtube.com" },
  { value: "www.apple.com", label: "ww.apple.com" },
  { value: "www.meta.com", label: "ww.meta.com" },
];

const Hero = () => {
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

        <Select
          className="m-auto w-[400px] border-spacing-[10px] border-red-700"
          options={options}
        />
      </div>
    </div>
  );
};

export default Hero;
