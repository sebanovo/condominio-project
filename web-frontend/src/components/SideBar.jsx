import { useState } from 'react';
import { SYSTEM_NAME } from '../constants/index';

function Sidebar({ activeSection, setActiveSection }) {
  const [openSections, setOpenSections] = useState({
    propiedades: true,
    servicios: false,
    seguridad: false,
  });

  const toggleSection = (section) => {
    setOpenSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const menuItems = [
    {
      id: 'dashboard',
      name: 'Dashboard',
      icon: '📊',
    },
    {
      id: 'propiedades',
      name: 'Gestión de Propiedades',
      icon: '🏠',
      children: [
        { id: 'casas', name: 'Casas/Departamentos' },
        { id: 'vehiculos', name: 'Vehículos' },
        { id: 'residentes', name: 'Residentes' },
      ],
    },
    {
      id: 'servicios',
      name: 'Servicios Comunes',
      icon: '🏊',
      children: [
        { id: 'areas-comunes', name: 'Áreas Comunes' },
        { id: 'reservas', name: 'Reservas' },
        { id: 'multas', name: 'Multas' },
      ],
    },
    {
      id: 'seguridad',
      name: 'Control de Acceso',
      icon: '🔒',
      children: [
        { id: 'ingresos-salidas', name: 'Ingresos y Salidas' },
        { id: 'extranjeros', name: 'Visitantes Extranjeros' },
      ],
    },
  ];

  return (
    <div className='flex w-64 flex-col bg-green-800 text-white'>
      <div className='flex items-center p-4'>
        <span className='text-xl font-bold'>🏢 {SYSTEM_NAME}</span>
      </div>

      <nav className='flex-1 overflow-y-auto pt-2'>
        <ul className='space-y-1 px-2'>
          {menuItems.map((item) => (
            <li key={item.id}>
              {item.children ? (
                <>
                  <button
                    onClick={() => toggleSection(item.id)}
                    className={`flex w-full items-center justify-between rounded-lg p-3 transition hover:bg-green-700 ${
                      openSections[item.id] ? 'bg-green-700' : ''
                    }`}
                  >
                    <div className='flex items-center'>
                      <span className='mr-3 text-lg'>{item.icon}</span>
                      <span>{item.name}</span>
                    </div>
                    <span
                      className={`transition-transform ${openSections[item.id] ? 'rotate-180 transform' : ''}`}
                    >
                      ▼
                    </span>
                  </button>

                  {openSections[item.id] && (
                    <ul className='mt-1 ml-6 space-y-1'>
                      {item.children.map((child) => (
                        <li key={child.id}>
                          <button
                            onClick={() => setActiveSection(child.id)}
                            className={`w-full rounded-lg p-2 pl-8 text-left transition hover:bg-green-700 ${
                              activeSection === child.id ? 'bg-green-600' : ''
                            }`}
                          >
                            {child.name}
                          </button>
                        </li>
                      ))}
                    </ul>
                  )}
                </>
              ) : (
                <button
                  onClick={() => setActiveSection(item.id)}
                  className={`flex w-full items-center rounded-lg p-3 transition hover:bg-green-700 ${
                    activeSection === item.id ? 'bg-green-600' : ''
                  }`}
                >
                  <span className='mr-3 text-lg'>{item.icon}</span>
                  <span>{item.name}</span>
                </button>
              )}
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}

export default Sidebar;
