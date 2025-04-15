// components/LoadingBar.jsx
import React from "react";

export default function LoadingBar({ progress = 0, status = "default" }) {
  const getColor = () => {
    switch (status) {
      case "success":
        return "bg-green-500";
      case "error":
        return "bg-red-500";
      default:
        return "bg-blue-600";
    }
  };

  return (
    <div className="w-full max-w-md mt-4">
      <div className="w-full bg-gray-200 rounded-full h-4 shadow-inner">
        <div
          className={`h-4 rounded-full transition-all duration-300 ease-in-out ${getColor()}`}
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      <p className="text-center text-sm text-gray-600 mt-1">{progress}%</p>
    </div>
  );
}
