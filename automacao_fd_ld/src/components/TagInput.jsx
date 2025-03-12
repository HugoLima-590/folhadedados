import React from "react";

export default function TagInput({ value, onChange }) {
    return (
        <input
            type="text"
            placeholder="Digite a tag de instrumento"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className="flex w-full text-md p-1.5 h-8 text-gray-500 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 mb-8 font-bold"
        />
    );
}
