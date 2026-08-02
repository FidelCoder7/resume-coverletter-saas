
import { createBrowserRouter } from 'react-router-dom'

import ProtectedRoute from '@/features/auth/components/ProtectedRoute'
import AppLayout from '@/layouts/AppLayout'
import PublicLayout from '@/layouts/PublicLayout'
import ComingSoon from '@/pages/ComingSoon'
import Dashboard from '@/pages/Dashboard'
import ForgotPassword from '@/pages/auth/ForgotPassword'
import Home from '@/pages/Home'
import Login from '@/pages/auth/Login'
import NotFound from '@/pages/NotFound'
import Register from '@/pages/auth/Register'
import ResetPassword from '@/pages/auth/ResetPassword'
import VerifyEmail from '@/pages/auth/VerifyEmail'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <PublicLayout />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: 'login',
        element: <Login />,
      },
      {
        path: 'register',
        element: <Register />,
      },
      {
        path: 'forgot-password',
        element: <ForgotPassword />,
      },
      {
        path: 'reset-password',
        element: <ResetPassword />,
      },
      {
        path: 'verify-email',
        element: <VerifyEmail />,
      },
    ],
  },
  {
    element: (
      <ProtectedRoute>
        <AppLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        path: 'dashboard',
        handle: {
          title: 'Dashboard',
        },
        element: <Dashboard />,
      },
      {
        path: 'resumes',
        handle: {
          title: 'Resumes',
        },
        element: (
          <ComingSoon
            title="Resumes"
            description="Resume management and AI-powered resume generation will be available here."
          />
        ),
      },
      {
        path: 'cover-letters',
        handle: {
          title: 'Cover Letters',
        },
        element: (
          <ComingSoon
            title="Cover Letters"
            description="Create and manage your AI-generated cover letters here."
          />
        ),
      },
      {
        path: 'ai',
        handle: {
          title: 'AI Tools',
        },
        element: (
          <ComingSoon
            title="AI Tools"
            description="AI-powered resume and cover letter tools are coming soon."
          />
        ),
      },
      {
        path: 'ats',
        handle: {
          title: 'ATS Optimization',
        },
        element: (
          <ComingSoon
            title="ATS Optimization"
            description="Optimize your resume for applicant tracking systems here."
          />
        ),
      },
      {
        path: 'billing',
        handle: {
          title: 'Billing',
        },
        element: (
          <ComingSoon
            title="Billing"
            description="Manage your subscription and billing information here."
          />
        ),
      },
      {
        path: 'profile',
        handle: {
          title: 'Profile',
        },
        element: (
          <ComingSoon
            title="Profile"
            description="Your profile management page is coming soon."
          />
        ),
      },
      {
        path: 'settings',
        handle: {
          title: 'Settings',
        },
        element: (
          <ComingSoon
            title="Settings"
            description="Application and account settings will be available here."
          />
        ),
      },
    ],
  },
  {
    path: '*',
    element: <NotFound />,
  },
])
