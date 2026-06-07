import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import { LandingPage } from './LandingPage';

describe('LandingPage', () => {
  it('renders the Hero section successfully', () => {
    render(
      <MemoryRouter>
        <LandingPage />
      </MemoryRouter>
    );
    
    // Check if the main heading is present
    const heading = screen.getByText(/Visualiza la Complejidad de los/i);
    expect(heading).toBeInTheDocument();

    // Check if the call to action buttons are present
    const startButton = screen.getByRole('button', { name: /Empezar Laboratorio/i });
    expect(startButton).toBeInTheDocument();

    const docButton = screen.getByRole('button', { name: /Ver Documentación/i });
    expect(docButton).toBeInTheDocument();

    // Check if the features are rendered
    expect(screen.getByText('Análisis Profundo')).toBeInTheDocument();
    expect(screen.getByText('Algoritmos Visuales')).toBeInTheDocument();
    expect(screen.getByText('Rendimiento Extremo')).toBeInTheDocument();
  });
});
