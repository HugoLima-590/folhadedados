import React, { useState } from 'react';
import Botao from './Botao';
import TagInput from './TagInput'; // Importando o TagInput

export default function TelaInputExcel() {
    const [file, setFile] = useState(null);
    const [tagInstrumento, setTagInstrumento] = useState(""); // Estado para armazenar a tag

    return (
        <div className='mb-20 p-20 w-200 h-95 bg-blue rounded-2xl container bg-gray-500'>
            <p className="mb-5 rounded-2xl flex justify-center p-3 text-bg font-medium text-black bg-white">
                Lista de Itens para Folha de Dados
            </p>
            <input
                className="flex w-full text-md p-1.5 text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50"
                id="file_input"
                type="file"
                accept=".xls,.xlsx,.xlsm,.csv"
                onChange={(e) => setFile(e.target.files[0])}
            />
            <p className="mt-2 text-sm text-gray-500">
                Arquivos suportados pelo sistema: xlsm, xlsx, xls ou csv.
            </p>

            <TagInput value={tagInstrumento} onChange={setTagInstrumento} />

            <Botao file={file} tagInstrumento={tagInstrumento} />
        </div>
    );
}
