import { createRootRoute, createRoute, createRouter, Outlet } from '@tanstack/react-router'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Layout from './components/layout/Layout'
import HomePage from './pages/HomePage'
import TeamsPage from './pages/TeamsPage'
import TeamDetailPage from './pages/TeamDetailPage'
import MatchesPage from './pages/MatchesPage'
import MatchDetailPage from './pages/MatchDetailPage'
import NewsPage from './pages/NewsPage'
import VideosPage from './pages/VideosPage'
import StatsPage from './pages/StatsPage'
import FantasyPage from './pages/FantasyPage'
import AboutPage from './pages/AboutPage'
import ContactPage from './pages/ContactPage'
import AuctionPage from './pages/AuctionPage'
import AdminPage from './pages/AdminPage'

// Create a root route
const rootRoute = createRootRoute({
  component: () => (
    <Layout>
      <Outlet />
    </Layout>
  ),
})

// Create individual routes
const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: HomePage,
})

const teamsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/teams',
  component: TeamsPage,
})

const teamDetailRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/teams/$teamId',
  component: TeamDetailPage,
})

const matchesRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/matches',
  component: MatchesPage,
})

const matchDetailRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/matches/$matchId',
  component: MatchDetailPage,
})

const newsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/news',
  component: NewsPage,
})

const newsDetailRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/news/$newsId',
  component: NewsPage,
})

const videosRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/videos',
  component: VideosPage,
})

const statsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/stats',
  component: StatsPage,
})

const fantasyRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/fantasy',
  component: FantasyPage,
})

const aboutRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/about',
  component: AboutPage,
})

const contactRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/contact',
  component: ContactPage,
})

const auctionRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/auction',
  component: AuctionPage,
})

const adminRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/admin',
  component: AdminPage,
})

// Create the route tree
const routeTree = rootRoute.addChildren([
  indexRoute,
  teamsRoute,
  teamDetailRoute,
  matchesRoute,
  matchDetailRoute,
  newsRoute,
  newsDetailRoute,
  videosRoute,
  statsRoute,
  fantasyRoute,
  aboutRoute,
  contactRoute,
  auctionRoute,
  adminRoute,
])

// Create the router
const router = createRouter({ 
  routeTree,
  defaultPreload: 'intent',
})

// Register the router instance for type safety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}

export default router
