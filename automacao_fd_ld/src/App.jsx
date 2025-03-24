import TelaInputExcel from "./components/TelaInputExcel";

export default function App() {
  return <div className="bg-slate-600 w-full h-screen flex flex-col items-center justify-center">
    <p className="mb-6 rounded-2xl flex justify-center p-4 font-bold text-black bg-white w-200">
      Lista de Intrumentos para Folha de Dados
    </p>
    <TelaInputExcel />
  </div>
}
