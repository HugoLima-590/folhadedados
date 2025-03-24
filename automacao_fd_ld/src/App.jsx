import TelaInputExcel from "./components/TelaInputExcel";

export default function App() {
  return (
    <div className="bg-slate-600 w-full h-screen flex flex-col items-center justify-center">
      <img
        src="/Texto_do_seu_parágrafo_20250324_114428_0000_page-0001-removebg-preview.png"
        alt="png"
        className="bg-gray-100 rounded-2xl w-50 h-20 object-cover object-center mb-20 -mt-10"
      />

      <p className="mb-6 rounded-2xl flex justify-center p-4 font-medium text-black bg-white w-200 text-2xl">
        Lista de Instrumentos para Folha de Dados
      </p>

      <TelaInputExcel />
    </div>
  );
}
