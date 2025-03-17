import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Button from '@mui/material/Button';

export default function Botao({ file, tagInstrumento }) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [disabled, setDisabled] = useState(true);
    const [downloadUrl, setDownloadUrl] = useState("");

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
    
            // Envia o arquivo para processamento
            const response = await axios.post("http://127.0.0.1:5000/", formData, {
                headers: { "Content-Type": "multipart/form-data" }
            });
    
            console.log("✅ Processamento concluído! Iniciando download...");
    
            // Captura o nome do arquivo retornado pelo backend
            const { filename } = response.data;
    
            if (!filename) {
                throw new Error("Nome do arquivo não retornado pelo servidor.");
            }
    
            // Faz o download do arquivo gerado
            const downloadResponse = await axios.get(`http://127.0.0.1:5000/download/${filename}`, {
                responseType: "blob", // Importante para baixar arquivos
            });
    
            // Cria um Blob e força o download
            const url = window.URL.createObjectURL(new Blob([downloadResponse.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", filename); // Usa o nome do arquivo correto
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
    
        } catch (err) {
            setError("Erro ao processar o arquivo.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center p-8">
            <Button 
                variant="contained" 
                className="text-white bg-amber-900 mt-4" 
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

            {error && <p className="text-red-500 mt-2">{error}</p>}
        </div>
    );
}
