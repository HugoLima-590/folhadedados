import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Button from '@mui/material/Button';

export default function Botao({ file, tagInstrumento }) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [disabled, setDisabled] = useState(true);

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
            await axios.post("http://127.0.0.1:5000/processar", formData, {
                headers: { "Content-Type": "multipart/form-data" }
            });

            console.log("✅ Processamento concluído! Iniciando download...");

            // Faz o download do arquivo FD_Preenchido.xlsm
            const link = document.createElement("a");
            link.href = "http://127.0.0.1:5000/download";
            link.setAttribute("download", "FD_Preenchido.xlsm");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
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
                disabled={disabled}
            >
                {loading ? "Processando..." : "Gerar e Baixar Documento"}
            </Button>
            {error && <p className="text-red-500 mt-2">{error}</p>}
        </div>
    );
}
