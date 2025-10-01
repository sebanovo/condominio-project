import { useState } from 'react';
import Sidebar from '../components/SideBar';
import { SYSTEM_NAME } from '../constants/index';
import { useNavigate } from 'react-router-dom';
import { server } from '../utils/server';
import {
  DashboardContent,
  CasasContent,
  VehiculosContent,
  AreasComunesContent,
  ReservasContent,
  MultasContent,
  ResidentesContent,
  IngresosSalidasContent,
  ExtranjerosContent,
  // Roles y permisos
  RolesContent,
} from './content';

export default function PanelAdminPage() {
  const [activeSection, setActiveSection] = useState('dashboard');
  const navigate = useNavigate();

  const handleLogOut = async () => {
    try {
      await server().logout();
      navigate('/login');
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
    }
  };

  const renderContent = () => {
    switch (activeSection) {
      case 'dashboard':
        return <DashboardContent />;
      case 'casas':
        return <CasasContent />;
      case 'vehiculos':
        return <VehiculosContent />;
      case 'areas-comunes':
        return <AreasComunesContent />;
      case 'reservas':
        return <ReservasContent />;
      case 'multas':
        return <MultasContent />;
      case 'residentes':
        return <ResidentesContent />;
      case 'ingresos-salidas':
        return <IngresosSalidasContent />;
      case 'extranjeros':
        return <ExtranjerosContent />;
      case 'roles':
        return <RolesContent />;
      default:
        return <DashboardContent />;
    }
  };

  return (
    <div className='flex h-screen bg-gray-100'>
      <Sidebar activeSection={activeSection} setActiveSection={setActiveSection} />
      <div className='flex flex-1 flex-col overflow-hidden'>
        <header className='bg-white shadow-sm'>
          <div className='flex items-center justify-between px-6 py-4'>
            <h1 className='text-2xl font-semibold text-gray-900'>
              Panel de Administración - {SYSTEM_NAME}
            </h1>
            <div className='flex items-center space-x-4'>
              <span className='text-gray-700'>Bienvenido, Admin</span>
              <button
                onClick={handleLogOut}
                className='rounded-lg bg-green-600 px-4 py-2 text-white transition hover:bg-green-700'
              >
                Cerrar sesión
              </button>
            </div>
          </div>
        </header>
        <main className='flex-1 overflow-y-auto p-6'>{renderContent()}</main>
      </div>
    </div>
  );
}
