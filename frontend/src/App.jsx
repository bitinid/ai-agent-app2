import { BrowserRouter as Router, Routes, Route } from 'react-router';
import Layout from './components/Layout';
import Research from './pages/Research';
import './App.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Research />} />
          <Route path="/research" element={<Research />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;