import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App Component', () => {
  test('renders translator title', () => {
    render(<App />);
    const titleElement = screen.getByText(/Professional Translator/i);
    expect(titleElement).toBeInTheDocument();
  });
});
