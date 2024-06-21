import HomePage from "./pages/HomePage";
import CreateInventoryItemPage from "./pages/CreateInventoryItemPage";

import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />}/>
        <Route path="/callback" element={<CreateInventoryItemPage />}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
