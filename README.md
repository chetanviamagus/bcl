# Bellandur Cricket League (BCL) Website

A modern, responsive cricket league website built with React, TypeScript, and Tailwind CSS, inspired by the IPL website structure and design.

## 🏏 Features

- **6 Competitive Teams**: MR Titans, Bellandur Monsters, Y K R Cricketers, Bellandur Sharks Cricketers, Super Giants Bellandur, and Royal Changlesrs Bellandur
- **Responsive Design**: Mobile-first approach with beautiful UI across all devices
- **Smooth Animations**: Framer Motion animations for enhanced user experience
- **Modern Tech Stack**: React 18, TypeScript, Vite, Tailwind CSS, TanStack Router & Query
- **Comprehensive Statistics**: Points table, player stats, and match results
- **News & Videos**: Latest updates and match highlights
- **Team Management**: Detailed team pages with player rosters

## 🚀 Tech Stack

- **Frontend**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: Semantic UI React
- **Icons**: Google Material Icons
- **Animations**: Framer Motion
- **State Management**: TanStack Query
- **Routing**: TanStack Router

## 📁 Project Structure

```
src/
├── components/
│   ├── layout/          # Header, Footer, Mobile Menu
│   └── home/            # Homepage components
├── pages/               # All page components
├── types/               # TypeScript interfaces
├── data/                # Mock data
├── hooks/               # Custom React hooks
├── services/            # API services
├── utils/               # Utility functions
└── assets/              # Images and static files
```

## 🎨 Design System

### Colors
- **Primary**: Cricket Green (#1B5E20)
- **Secondary**: Gold (#FFD700)
- **Accent**: White (#FFFFFF)
- **Text**: Dark Gray (#333333)
- **Background**: Light Gray (#F5F5F5)

### Typography
- **Headings**: Poppins
- **Body**: Inter
- **Scoreboard**: Orbitron

## 🏃‍♂️ Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bcl
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:3000`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 📱 Pages

- **Home**: Hero section, featured videos, team showcase, upcoming matches, points table
- **Teams**: All teams with statistics and player information
- **Team Detail**: Individual team pages with squad details
- **Matches**: Upcoming, live, and completed matches
- **News**: Latest news and announcements
- **Videos**: Match highlights and exclusive content
- **Stats**: Comprehensive statistics and leaderboards
- **Fantasy**: Fantasy cricket league (coming soon)
- **About**: League information and mission
- **Contact**: Contact form and information

## 🎯 Key Features

### Homepage
- Animated hero section with league branding
- Featured videos carousel
- Team showcase with statistics
- Upcoming matches with countdown
- Live points table
- Latest news section
- Player spotlight
- League statistics

### Team Pages
- Team logos and colors
- Captain and coach information
- Squad lists with player profiles
- Team statistics and performance
- Recent match results
- Home ground information

### Match Pages
- Live score updates (mock data)
- Match details and venue
- Team lineups
- Match statistics
- Commentary and updates

### Responsive Design
- Mobile-first approach
- Touch-friendly navigation
- Optimized images and videos
- Cross-browser compatibility

## 🎨 Animations

- Page transitions with Framer Motion
- Hover effects on interactive elements
- Staggered animations for content loading
- Cricket-themed loading animations
- Smooth scrolling and micro-interactions

## 📊 Data Structure

The application uses mock data with TypeScript interfaces for:
- Teams with statistics and player rosters
- Players with performance metrics
- Matches with scores and results
- News articles and videos
- League configuration

## 🔧 Customization

### Adding New Teams
1. Update the `mockTeams` array in `src/data/mockData.ts`
2. Add team logo to `public/images/teams/`
3. Update team colors in the data structure

### Modifying Styles
- Update `tailwind.config.js` for theme customization
- Modify component styles in individual files
- Update CSS variables in `src/index.css`

## 🚀 Deployment

The application is ready for deployment on platforms like:
- Vercel
- Netlify
- AWS Amplify
- GitHub Pages

Build the project:
```bash
npm run build
```

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Contact

For any queries or support, please contact:
- Email: info@bcl-cricket.com
- Phone: +91 98765 43210

---

**Bellandur Cricket League** - Premier Cricket League featuring 6 competitive teams