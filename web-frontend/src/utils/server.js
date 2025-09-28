export const server = () => ({
  validateSession: async () => {
    const response = await fetch('/api/v1/validate-session/', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Error validando sesión');
    }

    return response.json();
  },

  signUp: async (credentials) => {
    const response = await fetch('/api/v1/signup/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      throw new Error('Error en signup');
    }
    return response.json();
  },

  login: async (credentials) => {
    const response = await fetch('/api/v1/login/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      throw new Error('Error en login');
    }
    return response.json();
  },

  logout: async () => {
    const response = await fetch('/api/v1/logout/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Error en cerrar sesion');
    }
    return response.json();
  },
});
