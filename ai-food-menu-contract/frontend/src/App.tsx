import { Routes, Route } from "react-router-dom";
import MenuPage from "./pages/MenuPage";
import DishDetailPage from "./pages/DishPage";


function App() {
  return (
    <Routes>
      <Route path="/" element={<MenuPage />} />
      <Route path="/menu/:id" element={<DishDetailPage />} />
    </Routes>
  );
}

export default App;