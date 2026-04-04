export const API_URL = "http://127.0.0.1:8000";

export const fetchApi = async (endpoint, options = {}) => {
  const token = localStorage.getItem("accessToken");
  
  const headers = {
    ...options.headers,
  };
  
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  
  // No setear form-data automáticamente si es UploadFile (fetch lo hace solo con el boundary)
  if (!(options.body instanceof FormData) && !headers["Content-Type"]) {
      headers["Content-Type"] = "application/json";
  }

  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers
    });
    
    if (response.status === 401 && !endpoint.includes('/login')) {
      localStorage.removeItem("accessToken");
      window.location.href = "/login";
      throw new Error("Sesión expirada");
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const detail = errorData.detail;
      const errorMessage = typeof detail === 'string' 
        ? detail 
        : (Array.isArray(detail) ? detail.map(e => e.msg).join(', ') : JSON.stringify(detail || "Error en el servidor"));
      throw new Error(errorMessage);
    }

    // Para la descarga de plantillas
    if (options.isDownload) {
      return response;
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};
