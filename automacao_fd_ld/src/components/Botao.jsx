import React, { useState, useEffect } from "react";
import axios from "axios";
import Button from "@mui/material/Button";
import ErrorMessage from "../error/ErrorMessage";
import LoadingBar from "../components/LoadingBar";

export default function Botao({ file, tagInstrumento }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [disabled, setDisabled] = useState(true);
  const [progress, setProgress] = useState(0);
  const [statusMessage, setStatusMessage] = useState("");

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
      setProgress(0);
      setStatusMessage("Enviando arquivo...");

      const response = await axios.post("http://127.0.0.1:5000/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (event) => {
          if (event.lengthComputable) {
            const percent = Math.round((event.loaded * 50) / event.total); // Até 50%
            setProgress(percent);
          }
        },
      });

      setStatusMessage("Processando documento...");
      let simulatedProgress = 51;
      const interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 99) {
            clearInterval(interval);
            return prev;
          }
          return simulatedProgress++;
        });
      }, 100); // a cada 100ms sobe 1%

      const filename = response.data.filename;
      if (!filename) {
        throw new Error("Nome do arquivo não retornado pelo servidor.");
      }

      setStatusMessage("Baixando resultado...");

      const downloadResponse = await axios.get(
        `http://127.0.0.1:5000/download/${filename}`,
        {
          responseType: "blob",
        }
      );

      const blob = downloadResponse.data;
      const totalSize = blob.size;
      let loaded = 0;

      const reader = new Response(blob).body.getReader();
      const chunks = [];

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        chunks.push(value);
        loaded += value.length;

        const downloadProgress = Math.round((loaded * 50) / totalSize);
        setProgress(50 + downloadProgress);
      }
      setProgress(100);
      clearInterval(interval);

      const completeBlob = new Blob(chunks);
      const url = window.URL.createObjectURL(completeBlob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      setStatusMessage("✅ Documento gerado com sucesso!");
    } catch (err) {
      let errorMessage = "Erro desconhecido";

      if (err.response?.data?.error) {
        errorMessage = err.response.data.error;
      } else if (err.message.includes("Network Error")) {
        errorMessage = "Servidor não disponível, contate a equipe de TI.";
      } else {
        errorMessage = `Erro ao processar o arquivo: ${err.message}`;
      }

      setError(errorMessage);
      setStatusMessage("❌ Ocorreu um erro.");
    } finally {
      setLoading(false);
      setTimeout(() => {
        setProgress(0);
        setStatusMessage("");
      }, 5000); // limpa depois de 5 segundos
    }
  };

  return (
    <div className="flex flex-col items-center mt-4 w-full">
      <Button
        variant="contained"
        className="text-white bg-amber-900"
        onClick={handleUpload}
        disabled={disabled || loading}
      >
        {loading ? "Processando..." : "Gerar e Baixar Documento"}
      </Button>

      {loading || progress > 0 ? (
        <>
          <LoadingBar
            progress={progress}
            status={error ? "error" : progress === 100 ? "success" : "default"}
          />

          <p className="mt-2 text-sm text-gray-700">{statusMessage}</p>
        </>
      ) : null}

      <ErrorMessage message={error} />
    </div>
  );
}
