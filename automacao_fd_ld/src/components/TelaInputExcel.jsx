import React, { useState } from "react";
import Botao from "./Botao";
import TagInput from "./TagInput";

export default function TelaInputExcel() {
    const [file, setFile] = useState(null);
    const [tagInstrumento, setTagInstrumento] = useState("");

    return (
        <div className="mb-10 p-10 w-200 h-90 rounded-2xl container bg-gray-500">
            <header className="flex items-center justify-start gap-3 w-full -mt-5">
                <img
                    src="/ponto-de-exclamacao-em-um-circulo.png"
                    className="size-5 "
                />
                <p className="text-sm text-gray-300">
                    Aviso: Para que o sistema funcione corretamente, sua Lista de Instrumentos deve seguir o formato esperado.
                    Caso tenha dúvidas, baixe um exemplo:
                    <a
                        href="/Template Lista de Instrumentos.xlsx"
                        download
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-400 underline ml-1"
                    >
                        Baixar Template
                    </a>
                </p>
            </header>
        
            <input
                className="flex w-full text-md mt-8 p-1.5 text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50"
                id="file_input"
                type="file"
                accept=".xls,.xlsx,.xlsm,.csv"
                onChange={(e) => setFile(e.target.files[0])}
            />
            <p className="text-sm text-gray-300">
                Arquivos suportados pelo sistema: xlsm, xlsx, xls ou csv.
            </p>

            <TagInput value={tagInstrumento} onChange={setTagInstrumento} />

            <Botao file={file} tagInstrumento={tagInstrumento} />
        </div>
    );
}
