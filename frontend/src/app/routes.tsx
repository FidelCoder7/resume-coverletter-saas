import { createBrowserRouter, Navigate } from 'react-router-dom'

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
import AIWorkspace from '@/pages/ai/AIWorkspace'
import ATSOptimizer from '@/pages/ai/ATSOptimizer'
import AIUsageDashboard from '@/pages/ai/AIUsageDashboard'
import CoverLetterGenerator from '@/pages/ai/CoverLetterGenerator'
import ResumeGenerator from '@/pages/ai/ResumeGenerator'
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
import BillingDashboard from '@/pages/billing/BillingDashboard'
import BillingUsageDashboard from '@/pages/billing/UsageDashboard'
import PaymentDetails from '@/pages/billing/PaymentDetails'
import PaymentHistory from '@/pages/billing/PaymentHistory'
import Upgrade from '@/pages/billing/Upgrade'
import AdminRoute from '@/features/admin/components/AdminRoute'
import AdminLayout from '@/features/admin/components/AdminLayout'
import AdminDashboard from '@/pages/admin/AdminDashboard'
import AdminUsers from '@/pages/admin/AdminUsers'
import AdminUserDetails from '@/pages/admin/AdminUserDetails'
import AdminAuditLogs from '@/pages/admin/AdminAuditLogs'

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
        path: 'ai',
        handle: {
          title: 'AI Workspace',
        },
        element: <AIWorkspace />,
      },
      {
        path: 'ai/resume',
        handle: {
          title: 'AI Resume Generation',
        },
        element: <ResumeGenerator />,
      },
      {
        path: 'ai/cover-letter',
        handle: {
          title: 'AI Cover Letter',
        },
        element: <CoverLetterGenerator />,
      },
      {
        path: 'ai/ats',
        handle: {
          title: 'ATS Optimization',
        },
        element: <ATSOptimizer />,
      },
      {
        path: 'ai/usage',
        handle: {
          title: 'AI Usage History',
        },
        element: <AIUsageDashboard />,
      },

      {
        path: 'cover-letters',
        element: <Navigate to="/ai/cover-letter" replace />,
      },
      {
        path: 'ats',
        element: <Navigate to="/ai/ats" replace />,
      },

      {
        path: 'billing',
        handle: {
          title: 'Billing',
        },
        element: <BillingDashboard />,
      },
      {
        path: 'billing/usage',
        handle: {
          title: 'Usage Dashboard',
        },
        element: <BillingUsageDashboard />,
      },
      {
        path: 'billing/payments',
        handle: {
          title: 'Payment History',
        },
        element: <PaymentHistory />,
      },
      {
        path: 'billing/payments/:transactionId',
        handle: {
          title: 'Payment Details',
        },
        element: <PaymentDetails />,
      },

      {
        path: 'billing/upgrade',
        handle: {
          title: 'Upgrade to Pro',
        },
        element: <Upgrade />,
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
      {
        element: (
          <AdminRoute>
            <AdminLayout />
          </AdminRoute>
        ),
        children: [
          {
            path: 'admin',
            handle: {
              title: 'Admin Dashboard',
            },
            element: <AdminDashboard />,
          },
          {
            path: 'admin/users',
            handle: {
              title: 'User Management',
            },
            element: <AdminUsers />,
          },
          {
            path: 'admin/users/:userId',
            handle: {
              title: 'User Details',
            },
            element: <AdminUserDetails />,
          },
          {
            path: 'admin/audit-logs',
            handle: {
              title: 'Audit Logs',
            },
            element: <AdminAuditLogs />,
          },
        ],
      },
    ],
  },
  {
    path: '*',
    element: <NotFound />,
  },
])
