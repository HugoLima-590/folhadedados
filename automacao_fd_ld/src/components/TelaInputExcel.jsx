import React, { useState } from "react";
import Botao from "./Botao";
import TagInput from "./TagInput";

export default function TelaInputExcel() {
    const [file, setFile] = useState(null);
    const [tagInstrumento, setTagInstrumento] = useState("");

    return (
        <div className="mb-10 p-10 w-200 h-90 rounded-2xl container bg-gray-500">
            <p className="text-sm text-gray-300 -mt-7 flex">
                <img
                    src="/ponto-de-exclamacao-em-um-circulo.png"
                    alt="Aviso"
                    className="w-5 h-5 mr-2"
                />
                Aviso: Para que o sistema funcione corretamente, utilize uma Lista de Instrumentos no formato padrão.
            </p>

            <a
                href="/Template Lista de Instrumentos.xlsx"
                download
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 underline justify-center flex mt-1"
            >
                Baixar Template
            </a>

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
