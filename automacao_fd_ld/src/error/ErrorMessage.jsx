import React from "react";

export default function ErrorMessage({ message }) {
    if (!message) return null; // Não exibe nada se não houver erro

    return (
        <p className="text-red-500 mt-5 border border-red-500 p-2 rounded-md">
            ❌ {message}
        </p>
    );
}
