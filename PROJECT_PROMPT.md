# Bellandur Cricket League (BCL) Website Development Prompt

## Project Overview
Create a modern, responsive cricket league website for Bellandur Cricket League (BCL) with 6 teams, inspired by the IPL website structure and design.

## Tech Stack
- **Frontend Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: Semantic UI React
- **Icons**: Google Material Icons
- **Animations**: Framer Motion
- **State Management**: TanStack Query for data fetching
- **Routing**: TanStack Router

## Teams
1. **MR Titans**
2. **Bellandur Monsters** 
3. **Y K R Cricketers**
4. **Bellandur Sharks Cricketers**
5. **Super Giants Bellandur**
6. **Royal Changlesrs Bellandur**

## Website Structure (Based on IPL Reference)

### Header Navigation
- **MATCHES** - Upcoming and completed matches
- **POINTS TABLE** - Team standings and statistics
- **VIDEOS** - Match highlights, interviews, and exclusive content
  - Latest Videos
  - BCL Exclusive
  - Magic Moments
  - Highlights
  - Interviews
  - Press Conferences
- **TEAMS** - Individual team pages with player rosters
- **NEWS** - League news and announcements
  - All News
  - Announcements
  - Match Reports
- **FANTASY** - Fantasy cricket league
- **STATS** - Player and team statistics
  - Overall Stats
  - Head to Head
- **MORE** - Additional sections
  - Fan Contests
  - Photos
  - Mobile Products
  - Venues
  - About

### Homepage Sections
1. **Hero Banner** - Featured content with video/image carousel
2. **Featured Videos** - Latest highlights and exclusive content
3. **Team Showcase** - All 6 teams with logos and quick stats
4. **Upcoming Matches** - Next 3-4 matches with countdown timers
5. **Points Table** - Current standings
6. **Latest News** - Recent announcements and updates
7. **Player Spotlight** - Featured players
8. **Statistics** - Key league stats

### Team Pages
- Team logo and colors
- Squad list with player profiles
- Team statistics
- Recent match results
- Upcoming fixtures
- Team news and updates

### Match Pages
- Live score (if applicable)
- Match details and venue
- Team lineups
- Match statistics
- Commentary/updates
- Match photos and videos

## Design Requirements

### Color Scheme
- Primary: Cricket green (#1B5E20)
- Secondary: Gold (#FFD700)
- Accent: White (#FFFFFF)
- Text: Dark gray (#333333)
- Background: Light gray (#F5F5F5)

### Typography
- Headings: Inter or Poppins (Google Fonts)
- Body: Roboto (Google Fonts)
- Cricket-specific: Custom cricket scoreboard font

### Responsive Design
- Mobile-first approach
- Breakpoints: 320px, 768px, 1024px, 1440px
- Touch-friendly navigation for mobile
- Optimized images and videos

## Animation Requirements

### Page Transitions
- Smooth page-to-page transitions using Framer Motion
- Staggered animations for content loading
- Hover effects on interactive elements

### Component Animations
- **Cards**: Fade in with slide up effect
- **Buttons**: Scale and color transitions on hover
- **Images**: Lazy loading with fade in
- **Counters**: Animated number counting for statistics
- **Progress bars**: Animated progress for team standings
- **Video thumbnails**: Hover zoom and play button animation

### Micro-interactions
- Loading spinners with cricket ball animation
- Success/error notifications with slide animations
- Form validation with shake animations
- Tab switching with smooth transitions

## Features to Implement

### Core Features
1. **Responsive Navigation** - Collapsible mobile menu
2. **Match Scheduler** - Upcoming and completed matches
3. **Live Scoring** - Real-time match updates (mock data)
4. **Player Database** - Comprehensive player profiles
5. **Statistics Dashboard** - Team and player stats
6. **News Management** - Dynamic news and updates
7. **Photo Gallery** - Match and event photos
8. **Contact Form** - League contact information

### Advanced Features
1. **Fantasy League** - User registration and team management
2. **Live Chat** - Match discussion (optional)
3. **Social Media Integration** - Share buttons and feeds
4. **Search Functionality** - Search players, teams, matches
5. **Dark Mode Toggle** - Theme switching capability
6. **PWA Support** - Progressive Web App features

## Data Structure

### Team Data
```typescript
interface Team {
  id: string;
  name: string;
  shortName: string;
  logo: string;
  primaryColor: string;
  secondaryColor: string;
  captain: string;
  coach: string;
  founded: number;
  homeGround: string;
  players: Player[];
  stats: TeamStats;
}
```

### Player Data
```typescript
interface Player {
  id: string;
  name: string;
  role: 'Batsman' | 'Bowler' | 'All-rounder' | 'Wicket-keeper';
  teamId: string;
  jerseyNumber: number;
  age: number;
  nationality: string;
  battingStyle: string;
  bowlingStyle: string;
  stats: PlayerStats;
  photo: string;
}
```

### Match Data
```typescript
interface Match {
  id: string;
  homeTeam: string;
  awayTeam: string;
  venue: string;
  date: string;
  time: string;
  status: 'upcoming' | 'live' | 'completed';
  result?: string;
  score?: MatchScore;
}
```

## Performance Requirements
- **Lighthouse Score**: 90+ across all metrics
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **Time to Interactive**: < 3.5s

## SEO Requirements
- Meta tags for all pages
- Open Graph tags for social sharing
- Structured data markup for matches and teams
- Sitemap generation
- Robot.txt configuration

## Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development Guidelines

### Code Structure
```
src/
├── components/
│   ├── common/
│   ├── layout/
│   ├── teams/
│   ├── matches/
│   └── stats/
├── pages/
├── hooks/
├── services/
├── types/
├── utils/
└── assets/
```

### Naming Conventions
- Components: PascalCase (e.g., `TeamCard.tsx`)
- Files: kebab-case (e.g., `team-stats.ts`)
- Variables: camelCase
- Constants: UPPER_SNAKE_CASE

### Code Quality
- TypeScript strict mode
- ESLint configuration
- Prettier formatting
- Husky pre-commit hooks
- Unit tests with Vitest
- E2E tests with Playwright

## Deployment
- **Platform**: Vercel or Netlify
- **Domain**: Custom domain setup
- **CDN**: Image and video optimization
- **Analytics**: Google Analytics integration
- **Monitoring**: Error tracking with Sentry

## Timeline
- **Week 1**: Project setup, design system, and core components
- **Week 2**: Team pages, match pages, and data integration
- **Week 3**: Statistics, news, and advanced features
- **Week 4**: Testing, optimization, and deployment

## Success Criteria
1. Fully responsive design across all devices
2. Smooth animations and transitions
3. Fast loading times and performance
4. Intuitive user experience
5. Comprehensive cricket league functionality
6. Professional design matching IPL quality
7. Accessible and SEO-optimized

## Additional Notes
- Use mock data initially, with API integration planned for future
- Implement proper error handling and loading states
- Ensure accessibility compliance (WCAG 2.1)
- Include proper favicon and app icons
- Implement proper caching strategies
- Add proper error boundaries for React components
