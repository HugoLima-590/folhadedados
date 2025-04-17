export default function ErrorMessage({ message, code }) {
    if (!message) return null;

    return (
        <div className="text-red-600 mt-2 border border-red-500 p-2 rounded-md bg-red-50 shadow-sm">
            <strong>❌ Erro {code ? `[${code}]` : ""}:</strong> {message}
        </div>
    );
}
