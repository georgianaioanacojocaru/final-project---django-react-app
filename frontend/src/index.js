import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import * as serviceWorkerRegistration from './serviceWorkerRegistration';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter } from 'react-router-dom';
import AuthProvider from './context/AuthContext';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <AuthProvider>
  <BrowserRouter>
      <App />
    </BrowserRouter>
  </AuthProvider>

    );

serviceWorkerRegistration.unregister();

reportWebVitals();

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;