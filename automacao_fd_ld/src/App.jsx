import TelaInputExcel from "./components/TelaInputExcel";

export default function App() {
  return (
    <div className="bg-slate-600 w-full h-screen flex flex-col items-center justify-center">
      <img
        src="/Texto_do_seu_parágrafo_20250324_114428_0000_page-0001-removebg-preview.png"
        alt="png"
        className="bg-gray-100 rounded-2xl w-80 h-25 object-cover object-center mb-16 -mt-1"
      />
      <TelaInputExcel />
    </div>
  );
}
