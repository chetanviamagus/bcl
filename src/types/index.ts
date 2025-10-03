// Team and Player Types
export interface Team {
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

export interface Player {
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

export interface TeamStats {
  matchesPlayed: number;
  matchesWon: number;
  matchesLost: number;
  points: number;
  netRunRate: number;
  position: number;
}

export interface PlayerStats {
  matches: number;
  runs: number;
  wickets: number;
  catches: number;
  strikeRate: number;
  economy: number;
  average: number;
}

// Match Types
export interface Match {
  id: string;
  homeTeam: string;
  awayTeam: string;
  venue: string;
  date: string;
  time: string;
  status: 'upcoming' | 'live' | 'completed';
  result?: string;
  score?: MatchScore;
  tossWinner?: string;
  tossDecision?: 'bat' | 'bowl';
}

export interface MatchScore {
  homeTeam: {
    runs: number;
    wickets: number;
    overs: number;
  };
  awayTeam: {
    runs: number;
    wickets: number;
    overs: number;
  };
  currentInnings?: 'home' | 'away';
  requiredRunRate?: number;
  target?: number;
}

// News and Content Types
export interface NewsArticle {
  id: string;
  title: string;
  content: string;
  excerpt: string;
  author: string;
  publishedAt: string;
  category: 'news' | 'announcement' | 'match-report';
  imageUrl: string;
  tags: string[];
}

export interface Video {
  id: string;
  title: string;
  description: string;
  thumbnail: string;
  duration: string;
  views: number;
  category: 'highlights' | 'interview' | 'exclusive' | 'magic-moments';
  publishedAt: string;
  url: string;
}

// Navigation Types
export interface NavItem {
  label: string;
  href: string;
  children?: NavItem[];
}

// API Response Types
export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// Form Types
export interface ContactForm {
  name: string;
  email: string;
  subject: string;
  message: string;
}

// Theme Types
export interface Theme {
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  text: string;
}

// Animation Types
export interface AnimationVariants {
  hidden: object;
  visible: object;
  exit?: object;
}

// Component Props Types
export interface BaseComponentProps {
  className?: string;
  children?: React.ReactNode;
}

export interface TeamCardProps extends BaseComponentProps {
  team: Team;
  onClick?: () => void;
}

export interface PlayerCardProps extends BaseComponentProps {
  player: Player;
  showStats?: boolean;
}

export interface MatchCardProps extends BaseComponentProps {
  match: Match;
  showDetails?: boolean;
}

// League Configuration
export interface LeagueConfig {
  name: string;
  season: string;
  totalTeams: number;
  totalMatches: number;
  startDate: string;
  endDate: string;
  venues: string[];
  sponsors: Sponsor[];
}

export interface Sponsor {
  id: string;
  name: string;
  logo: string;
  category: 'title' | 'associate' | 'official';
  website?: string;
}

// Auction Types
export interface AuctionPlayer {
  id: string;
  name: string;
  role: 'Batsman' | 'Bowler' | 'All-rounder' | 'Wicket-keeper';
  age: number;
  nationality: string;
  battingStyle: string;
  bowlingStyle: string;
  basePrice: number;
  currentBid: number;
  soldTo?: string; // Team ID
  soldPrice?: number;
  status: 'available' | 'sold' | 'unsold';
  photo: string;
  stats: PlayerStats;
  previousTeam?: string;
}

export interface Bid {
  id: string;
  playerId: string;
  teamId: string;
  amount: number;
  timestamp: string;
  isWinning: boolean;
}

export interface AuctionSession {
  id: string;
  name: string;
  date: string;
  startTime: string;
  endTime?: string;
  status: 'upcoming' | 'live' | 'completed';
  totalPlayers: number;
  soldPlayers: number;
  totalAmount: number;
  currentPlayer?: string;
}

export interface TeamBudget {
  teamId: string;
  teamName: string;
  totalBudget: number;
  spentAmount: number;
  remainingBudget: number;
  playersBought: number;
}
