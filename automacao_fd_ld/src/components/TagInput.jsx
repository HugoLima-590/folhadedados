import React from "react";

export default function TagInput({ value, onChange }) {
    return (
        <>
        <input
        type="text"
        placeholder="Digite a tag de instrumento"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="flex w-full text-md mt-8 p-1.5 h-8 text-gray-500 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 mb-8 font-bold"
        />
        <p className="text-sm text-gray-300 -mt-7 font-medium">
            Digite as iniciais da Tag presente na planilha "Listas de Instrumentos".
        </p>
    </>
    );
}
