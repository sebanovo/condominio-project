// content/DashboardContent.jsx
import { useState, useEffect } from 'react';

export default function DashboardContent() {
  const [stats, setStats] = useState({
    totalResidentes: 0,
    totalCasas: 0,
    reservasHoy: 0,
    multasPendientes: 0,
  });

  useEffect(() => {
    // Aquí cargarías los datos del dashboard
    // Por ahora datos de ejemplo
    setStats({
      totalResidentes: 150,
      totalCasas: 75,
      reservasHoy: 12,
      multasPendientes: 5,
    });
  }, []);

  return (
    <div className='space-y-6'>
      <h1 className='text-3xl font-bold text-gray-900'>Dashboard del Condominio</h1>
      {/* Estadísticas */}
      <div className='grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4'>
        <div className='rounded-lg bg-white p-6 shadow'>
          <div className='flex items-center'>
            <div className='rounded-full bg-green-100 p-3'>
              <span className='text-2xl'>👥</span>
            </div>
            <div className='ml-4'>
              <p className='text-sm font-medium text-gray-600'>Total Residentes</p>
              <p className='text-2xl font-bold text-gray-900'>{stats.totalResidentes}</p>
            </div>
          </div>
        </div>

        <div className='rounded-lg bg-white p-6 shadow'>
          <div className='flex items-center'>
            <div className='rounded-full bg-blue-100 p-3'>
              <span className='text-2xl'>🏠</span>
            </div>
            <div className='ml-4'>
              <p className='text-sm font-medium text-gray-600'>Total Casas</p>
              <p className='text-2xl font-bold text-gray-900'>{stats.totalCasas}</p>
            </div>
          </div>
        </div>

        <div className='rounded-lg bg-white p-6 shadow'>
          <div className='flex items-center'>
            <div className='rounded-full bg-amber-100 p-3'>
              <span className='text-2xl'>📅</span>
            </div>
            <div className='ml-4'>
              <p className='text-sm font-medium text-gray-600'>Reservas Hoy</p>
              <p className='text-2xl font-bold text-gray-900'>{stats.reservasHoy}</p>
            </div>
          </div>
        </div>

        <div className='rounded-lg bg-white p-6 shadow'>
          <div className='flex items-center'>
            <div className='rounded-full bg-red-100 p-3'>
              <span className='text-2xl'>⚠️</span>
            </div>
            <div className='ml-4'>
              <p className='text-sm font-medium text-gray-600'>Multas Pendientes</p>
              <p className='text-2xl font-bold text-gray-900'>{stats.multasPendientes}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Secciones rápidas */}
      <div className='grid grid-cols-1 gap-6 lg:grid-cols-2'>
        <div className='rounded-lg bg-white p-6 shadow'>
          <h2 className='mb-4 text-xl font-semibold'>Actividad Reciente</h2>
          <div className='space-y-3'>
            <div className='flex items-center justify-between border-b pb-2'>
              <span className='text-sm'>Nuevo ingreso registrado</span>
              <span className='text-xs text-gray-500'>Hace 5 min</span>
            </div>
            <div className='flex items-center justify-between border-b pb-2'>
              <span className='text-sm'>Reserva de piscina confirmada</span>
              <span className='text-xs text-gray-500'>Hace 15 min</span>
            </div>
            <div className='flex items-center justify-between border-b pb-2'>
              <span className='text-sm'>Multa registrada</span>
              <span className='text-xs text-gray-500'>Hace 1 hora</span>
            </div>
          </div>
        </div>

        <div className='rounded-lg bg-white p-6 shadow'>
          <h2 className='mb-4 text-xl font-semibold'>Acciones Rápidas</h2>
          <div className='grid grid-cols-2 gap-4'>
            <button className='rounded-lg bg-green-600 px-4 py-3 text-white transition hover:bg-green-700'>
              Registrar Ingreso
            </button>
            <button className='rounded-lg bg-blue-600 px-4 py-3 text-white transition hover:bg-blue-700'>
              Nueva Reserva
            </button>
            <button className='rounded-lg bg-amber-600 px-4 py-3 text-white transition hover:bg-amber-700'>
              Registrar Multa
            </button>
            <button className='rounded-lg bg-purple-600 px-4 py-3 text-white transition hover:bg-purple-700'>
              Agregar Visitante
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
