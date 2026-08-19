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
import CreateResume from '@/pages/resumes/CreateResume'
import EditResume from '@/pages/resumes/EditResume'
import ResumeDashboard from '@/pages/resumes/ResumeDashboard'
import ResumeDetails from '@/pages/resumes/ResumeDetails'
import ResumeManager from '@/pages/resumes/ResumeManager'
import ExperienceManagement from '@/pages/resumes/ExperienceManagement'
import EducationManagement from '@/pages/resumes/EducationManagement'
import SkillsManagement from '@/pages/resumes/SkillsManagement'
import ProjectsManagement from '@/pages/resumes/ProjectsManagement'
import CertificationsManagement from '@/pages/resumes/CertificationsManagement'

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
        element: <ResumeDashboard />,
      },
      {
        path: 'resumes/new',
        handle: {
          title: 'Create Resume',
        },
        element: <CreateResume />,
      },
      {
        path: 'resumes/:resumeId/experience',
        handle: {
          title: 'Experience Management',
        },
        element: <ExperienceManagement />,
      },

      {
        path: 'resumes/:resumeId/education',
        handle: {
          title: 'Education Management',
        },
        element: <EducationManagement />,
      },
      {
        path: 'resumes/:resumeId/skills',
        handle: {
          title: 'Skills Management',
        },
        element: <SkillsManagement />,
      },
      {
        path: 'resumes/:resumeId/projects',
        handle: {
          title: 'Projects Management',
        },
        element: <ProjectsManagement />,
      },
      {
        path: 'resumes/:resumeId/certifications',
        handle: {
          title: 'Certifications Management',
        },
        element: <CertificationsManagement />,
      },
      {
        path: 'resumes/:resumeId',
        handle: {
          title: 'Resume Details',
        },
        element: <ResumeDetails />,
      },
      {
        path: 'resumes/:resumeId/manage',
        handle: {
          title: 'Resume Manager',
        },
        element: <ResumeManager />,
      },
      {
        path: 'resumes/:resumeId/edit',
        handle: {
          title: 'Edit Resume',
        },
        element: <EditResume />,
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
