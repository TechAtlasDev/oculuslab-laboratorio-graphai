import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { LandingPage } from "./pages/LandingPage"
import { GraphExplorerPage } from "./pages/GraphExplorerPage"

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/explorer" element={<GraphExplorerPage />} />
      </Routes>
    </BrowserRouter>
  )
}