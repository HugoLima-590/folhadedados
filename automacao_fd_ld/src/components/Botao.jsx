import React, { useState, useEffect } from "react";
import axios from "axios";
import Button from "@mui/material/Button";
import ErrorMessage from "../error/ErrorMessage"; // Importa o componente de erro

export default function Botao({ file, tagInstrumento }) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [disabled, setDisabled] = useState(true);
    const [downloadUrl] = useState("");

    useEffect(() => {
        setDisabled(!(file && tagInstrumento));
    }, [file, tagInstrumento]);

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("tag_instrumento", tagInstrumento);

        try {
            setLoading(true);
            setError(null);

            const response = await axios.post("http://127.0.0.1:5000/", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            console.log("✅ Processamento concluído! Iniciando download...");
            const { filename } = response.data;

            if (!filename) {
                throw new Error("Nome do arquivo não retornado pelo servidor.");
            }

            const downloadResponse = await axios.get(`http://127.0.0.1:5000/download/${filename}`, {
                responseType: "blob",
            });

            const url = window.URL.createObjectURL(new Blob([downloadResponse.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", filename);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (err) {
            let errorMessage = "Erro desconhecido";

            if (err.response?.data?.error) {
                errorMessage = err.response.data.error;
            } else if (err.message.includes("Network Error")) {
                errorMessage = "Servidor não disponível, contate a equipe de TI.";
            } else if (err.message) {
                errorMessage = `Erro ao processar o arquivo: ${err.message}`;
            }

            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center mt-4">
            <Button
                variant="contained"
                className="text-white bg-amber-900"
                onClick={handleUpload}
                disabled={disabled || loading}
            >
                {loading ? "Processando..." : "Gerar e Baixar Documento"}
            </Button>

            {downloadUrl && (
                <a href={downloadUrl} download className="mt-4 text-blue-500 underline">
                    📥 Baixar Arquivo
                </a>
            )}
            <ErrorMessage 
            message={error} 
            />
        </div>
    );
}
