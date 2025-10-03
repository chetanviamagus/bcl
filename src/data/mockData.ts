import { Team, Player, Match, NewsArticle, Video, LeagueConfig, AuctionPlayer, AuctionSession, TeamBudget } from '@/types';

// Mock Teams Data
export const mockTeams: Team[] = [
  {
    id: 'mr-titans',
    name: 'MR Titans',
    shortName: 'MRT',
    logo: '/images/teams/mr-titans.png',
    primaryColor: '#1B5E20',
    secondaryColor: '#FFD700',
    captain: 'Rahul Sharma',
    coach: 'Vikram Singh',
    founded: 2020,
    homeGround: 'Bellandur Cricket Ground',
    players: [],
    stats: {
      matchesPlayed: 8,
      matchesWon: 6,
      matchesLost: 2,
      points: 12,
      netRunRate: 0.85,
      position: 1
    }
  },
  {
    id: 'bellandur-monsters',
    name: 'Bellandur Monsters',
    shortName: 'BM',
    logo: '/images/teams/bellandur-monsters.png',
    primaryColor: '#8B0000',
    secondaryColor: '#FFD700',
    captain: 'Arjun Patel',
    coach: 'Suresh Kumar',
    founded: 2019,
    homeGround: 'Bellandur Sports Complex',
    players: [],
    stats: {
      matchesPlayed: 8,
      matchesWon: 5,
      matchesLost: 3,
      points: 10,
      netRunRate: 0.42,
      position: 2
    }
  },
  {
    id: 'ykr-cricketers',
    name: 'Y K R Cricketers',
    shortName: 'YKR',
    logo: '/images/teams/ykr-cricketers.png',
    primaryColor: '#0066CC',
    secondaryColor: '#FFFFFF',
    captain: 'Kiran Reddy',
    coach: 'Rajesh Gupta',
    founded: 2021,
    homeGround: 'Y K R Ground',
    players: [],
    stats: {
      matchesPlayed: 8,
      matchesWon: 4,
      matchesLost: 4,
      points: 8,
      netRunRate: -0.15,
      position: 3
    }
  },
  {
    id: 'bellandur-sharks',
    name: 'Bellandur Sharks Cricketers',
    shortName: 'BSC',
    logo: '/images/teams/bellandur-sharks.png',
    primaryColor: '#FF6B35',
    secondaryColor: '#1B5E20',
    captain: 'Suresh Yadav',
    coach: 'Amit Kumar',
    founded: 2020,
    homeGround: 'Sharks Arena',
    players: [],
    stats: {
      matchesPlayed: 8,
      matchesWon: 4,
      matchesLost: 4,
      points: 8,
      netRunRate: 0.12,
      position: 4
    }
  },
  {
    id: 'super-giants-bellandur',
    name: 'Super Giants Bellandur',
    shortName: 'SGB',
    logo: '/images/teams/super-giants.png',
    primaryColor: '#800080',
    secondaryColor: '#FFD700',
    captain: 'Vikram Joshi',
    coach: 'Naveen Kumar',
    founded: 2019,
    homeGround: 'Giants Stadium',
    players: [],
    stats: {
      matchesPlayed: 8,
      matchesWon: 3,
      matchesLost: 5,
      points: 6,
      netRunRate: -0.25,
      position: 5
    }
  },
  {
    id: 'royal-changlesrs-bellandur',
    name: 'Royal Changlesrs Bellandur',
    shortName: 'RCB',
    logo: '/images/teams/royal-changlesrs.png',
    primaryColor: '#FF0000',
    secondaryColor: '#FFD700',
    captain: 'Rohit Verma',
    coach: 'Sanjay Singh',
    founded: 2021,
    homeGround: 'Royal Ground',
    players: [],
    stats: {
      matchesPlayed: 8,
      matchesWon: 2,
      matchesLost: 6,
      points: 4,
      netRunRate: -0.68,
      position: 6
    }
  }
];

// Mock Players Data
export const mockPlayers: Player[] = [
  // MR Titans Players
  {
    id: 'rahul-sharma',
    name: 'Rahul Sharma',
    role: 'Batsman',
    teamId: 'mr-titans',
    jerseyNumber: 7,
    age: 28,
    nationality: 'Indian',
    battingStyle: 'Right-handed',
    bowlingStyle: 'Right-arm medium',
    stats: {
      matches: 8,
      runs: 456,
      wickets: 2,
      catches: 5,
      strikeRate: 142.5,
      economy: 7.2,
      average: 57.0
    },
    photo: '/images/players/rahul-sharma.jpg'
  },
  {
    id: 'vikram-singh',
    name: 'Vikram Singh',
    role: 'All-rounder',
    teamId: 'mr-titans',
    jerseyNumber: 12,
    age: 25,
    nationality: 'Indian',
    battingStyle: 'Left-handed',
    bowlingStyle: 'Left-arm spin',
    stats: {
      matches: 8,
      runs: 234,
      wickets: 8,
      catches: 3,
      strikeRate: 128.5,
      economy: 6.8,
      average: 29.25
    },
    photo: '/images/players/vikram-singh.jpg'
  },
  // Bellandur Monsters Players
  {
    id: 'arjun-patel',
    name: 'Arjun Patel',
    role: 'Batsman',
    teamId: 'bellandur-monsters',
    jerseyNumber: 10,
    age: 30,
    nationality: 'Indian',
    battingStyle: 'Right-handed',
    bowlingStyle: 'Right-arm off-spin',
    stats: {
      matches: 8,
      runs: 389,
      wickets: 1,
      catches: 4,
      strikeRate: 135.2,
      economy: 8.1,
      average: 48.6
    },
    photo: '/images/players/arjun-patel.jpg'
  },
  {
    id: 'suresh-kumar',
    name: 'Suresh Kumar',
    role: 'Bowler',
    teamId: 'bellandur-monsters',
    jerseyNumber: 15,
    age: 27,
    nationality: 'Indian',
    battingStyle: 'Right-handed',
    bowlingStyle: 'Right-arm fast',
    stats: {
      matches: 8,
      runs: 45,
      wickets: 12,
      catches: 2,
      strikeRate: 95.2,
      economy: 5.8,
      average: 3.75
    },
    photo: '/images/players/suresh-kumar.jpg'
  },
  // Y K R Cricketers Players
  {
    id: 'kiran-reddy',
    name: 'Kiran Reddy',
    role: 'Wicket-keeper',
    teamId: 'ykr-cricketers',
    jerseyNumber: 1,
    age: 26,
    nationality: 'Indian',
    battingStyle: 'Left-handed',
    bowlingStyle: 'N/A',
    stats: {
      matches: 8,
      runs: 312,
      wickets: 0,
      catches: 12,
      strikeRate: 125.8,
      economy: 0,
      average: 39.0
    },
    photo: '/images/players/kiran-reddy.jpg'
  },
  // Add more players as needed...
];

// Mock Matches Data
export const mockMatches: Match[] = [
  {
    id: 'match-1',
    homeTeam: 'MR Titans',
    awayTeam: 'Bellandur Monsters',
    venue: 'Bellandur Cricket Ground',
    date: '2024-01-15',
    time: '14:00',
    status: 'completed',
    result: 'MR Titans won by 25 runs',
    score: {
      homeTeam: { runs: 180, wickets: 6, overs: 20 },
      awayTeam: { runs: 155, wickets: 8, overs: 20 }
    },
    tossWinner: 'MR Titans',
    tossDecision: 'bat'
  },
  {
    id: 'match-2',
    homeTeam: 'Y K R Cricketers',
    awayTeam: 'Bellandur Sharks Cricketers',
    venue: 'Y K R Ground',
    date: '2024-01-20',
    time: '14:00',
    status: 'upcoming',
    tossWinner: 'Y K R Cricketers',
    tossDecision: 'bat'
  },
  {
    id: 'match-3',
    homeTeam: 'Super Giants Bellandur',
    awayTeam: 'Royal Changlesrs Bellandur',
    venue: 'Giants Stadium',
    date: '2024-01-25',
    time: '14:00',
    status: 'live',
    score: {
      homeTeam: { runs: 120, wickets: 3, overs: 12 },
      awayTeam: { runs: 0, wickets: 0, overs: 0 }
    },
    tossWinner: 'Super Giants Bellandur',
    tossDecision: 'bat'
  }
];

// Mock News Articles
export const mockNews: NewsArticle[] = [
  {
    id: 'news-1',
    title: 'MR Titans Lead the Points Table After Stunning Victory',
    content: 'MR Titans continued their impressive form with a comprehensive victory over Bellandur Monsters...',
    excerpt: 'MR Titans maintained their position at the top of the table with another convincing win.',
    author: 'Sports Reporter',
    publishedAt: '2024-01-16T10:00:00Z',
    category: 'match-report',
    imageUrl: '/images/news/mr-titans-victory.jpg',
    tags: ['MR Titans', 'Victory', 'Points Table']
  },
  {
    id: 'news-2',
    title: 'BCL 2024 Season Schedule Announced',
    content: 'The complete schedule for Bellandur Cricket League 2024 has been released...',
    excerpt: 'All 6 teams will compete in a round-robin format with playoffs to follow.',
    author: 'BCL Admin',
    publishedAt: '2024-01-10T09:00:00Z',
    category: 'announcement',
    imageUrl: '/images/news/schedule-announcement.jpg',
    tags: ['Schedule', '2024 Season', 'Announcement']
  }
];

// Mock Videos
export const mockVideos: Video[] = [
  {
    id: 'video-1',
    title: 'MR Titans vs Bellandur Monsters - Match Highlights',
    description: 'Watch the best moments from the thrilling encounter between MR Titans and Bellandur Monsters.',
    thumbnail: '/images/videos/match-highlights-1.jpg',
    duration: '5:32',
    views: 15420,
    category: 'highlights',
    publishedAt: '2024-01-16T15:30:00Z',
    url: '/videos/match-highlights-1.mp4'
  },
  {
    id: 'video-2',
    title: 'Rahul Sharma - Player of the Match Interview',
    description: 'MR Titans captain Rahul Sharma speaks about his team\'s performance and upcoming matches.',
    thumbnail: '/images/videos/rahul-sharma-interview.jpg',
    duration: '3:45',
    views: 8920,
    category: 'interview',
    publishedAt: '2024-01-16T18:00:00Z',
    url: '/videos/rahul-sharma-interview.mp4'
  }
];

// League Configuration
export const leagueConfig: LeagueConfig = {
  name: 'Bellandur Cricket League',
  season: '2024',
  totalTeams: 6,
  totalMatches: 30,
  startDate: '2024-01-01',
  endDate: '2024-03-31',
  venues: [
    'Bellandur Cricket Ground',
    'Bellandur Sports Complex',
    'Y K R Ground',
    'Sharks Arena',
    'Giants Stadium',
    'Royal Ground'
  ],
  sponsors: [
    {
      id: 'sponsor-1',
      name: 'TATA',
      logo: '/images/sponsors/tata.png',
      category: 'title'
    },
    {
      id: 'sponsor-2',
      name: 'My11Circle',
      logo: '/images/sponsors/my11circle.png',
      category: 'associate'
    }
  ]
};

// Helper function to get team by ID
export function getTeamById(teamId: string): Team | undefined {
  return mockTeams.find(team => team.id === teamId);
}

// Helper function to get players by team ID
export function getPlayersByTeamId(teamId: string): Player[] {
  return mockPlayers.filter(player => player.id === teamId);
}

// Helper function to get upcoming matches
export function getUpcomingMatches(): Match[] {
  return mockMatches.filter(match => match.status === 'upcoming');
}

// Helper function to get completed matches
export function getCompletedMatches(): Match[] {
  return mockMatches.filter(match => match.status === 'completed');
}

// Helper function to get live matches
export function getLiveMatches(): Match[] {
  return mockMatches.filter(match => match.status === 'live');
}

// Mock Auction Data
export const mockAuctionPlayers: AuctionPlayer[] = [
  {
    id: 'auction-player-1',
    name: 'Sachin Kumar',
    role: 'Batsman',
    age: 24,
    nationality: 'Indian',
    battingStyle: 'Right-handed',
    bowlingStyle: 'Right-arm medium',
    basePrice: 50000,
    currentBid: 75000,
    status: 'available',
    photo: '/images/auction/sachin-kumar.jpg',
    stats: {
      matches: 15,
      runs: 450,
      wickets: 2,
      catches: 8,
      strikeRate: 145.2,
      economy: 7.5,
      average: 45.0
    },
    previousTeam: 'Delhi Daredevils'
  },
  {
    id: 'auction-player-2',
    name: 'Rohit Verma',
    role: 'All-rounder',
    age: 26,
    nationality: 'Indian',
    battingStyle: 'Left-handed',
    bowlingStyle: 'Left-arm spin',
    basePrice: 30000,
    currentBid: 45000,
    status: 'available',
    photo: '/images/auction/rohit-verma.jpg',
    stats: {
      matches: 12,
      runs: 280,
      wickets: 15,
      catches: 5,
      strikeRate: 135.8,
      economy: 6.2,
      average: 23.3
    },
    previousTeam: 'Mumbai Indians'
  },
  {
    id: 'auction-player-3',
    name: 'Virat Singh',
    role: 'Bowler',
    age: 22,
    nationality: 'Indian',
    battingStyle: 'Right-handed',
    bowlingStyle: 'Right-arm fast',
    basePrice: 40000,
    currentBid: 0,
    status: 'available',
    photo: '/images/auction/virat-singh.jpg',
    stats: {
      matches: 8,
      runs: 45,
      wickets: 18,
      catches: 3,
      strikeRate: 85.2,
      economy: 5.5,
      average: 2.5
    },
    previousTeam: 'Royal Challengers Bangalore'
  },
  {
    id: 'auction-player-4',
    name: 'MS Dhoni Jr.',
    role: 'Wicket-keeper',
    age: 28,
    nationality: 'Indian',
    battingStyle: 'Right-handed',
    bowlingStyle: 'N/A',
    basePrice: 60000,
    currentBid: 90000,
    status: 'sold',
    soldTo: 'mr-titans',
    soldPrice: 90000,
    photo: '/images/auction/ms-dhoni-jr.jpg',
    stats: {
      matches: 20,
      runs: 520,
      wickets: 0,
      catches: 25,
      strikeRate: 125.5,
      economy: 0,
      average: 34.7
    },
    previousTeam: 'Chennai Super Kings'
  },
  {
    id: 'auction-player-5',
    name: 'Ravindra Jadeja Jr.',
    role: 'All-rounder',
    age: 25,
    nationality: 'Indian',
    battingStyle: 'Left-handed',
    bowlingStyle: 'Left-arm orthodox',
    basePrice: 70000,
    currentBid: 0,
    status: 'available',
    photo: '/images/auction/ravindra-jadeja-jr.jpg',
    stats: {
      matches: 18,
      runs: 380,
      wickets: 22,
      catches: 12,
      strikeRate: 140.2,
      economy: 6.8,
      average: 21.1
    },
    previousTeam: 'Gujarat Titans'
  }
];

export const mockAuctionSession: AuctionSession = {
  id: 'auction-2024',
  name: 'BCL 2024 Player Auction',
  date: '2024-02-15',
  startTime: '10:00',
  endTime: '18:00',
  status: 'live',
  totalPlayers: 50,
  soldPlayers: 12,
  totalAmount: 2500000,
  currentPlayer: 'auction-player-1'
};

export const mockTeamBudgets: TeamBudget[] = [
  {
    teamId: 'mr-titans',
    teamName: 'MR Titans',
    totalBudget: 500000,
    spentAmount: 180000,
    remainingBudget: 320000,
    playersBought: 3
  },
  {
    teamId: 'bellandur-monsters',
    teamName: 'Bellandur Monsters',
    totalBudget: 500000,
    spentAmount: 220000,
    remainingBudget: 280000,
    playersBought: 4
  },
  {
    teamId: 'ykr-cricketers',
    teamName: 'Y K R Cricketers',
    totalBudget: 500000,
    spentAmount: 150000,
    remainingBudget: 350000,
    playersBought: 2
  },
  {
    teamId: 'bellandur-sharks',
    teamName: 'Bellandur Sharks',
    totalBudget: 500000,
    spentAmount: 200000,
    remainingBudget: 300000,
    playersBought: 3
  },
  {
    teamId: 'super-giants-bellandur',
    teamName: 'Super Giants Bellandur',
    totalBudget: 500000,
    spentAmount: 120000,
    remainingBudget: 380000,
    playersBought: 2
  },
  {
    teamId: 'royal-changlesrs-bellandur',
    teamName: 'Royal Changlesrs Bellandur',
    totalBudget: 500000,
    spentAmount: 190000,
    remainingBudget: 310000,
    playersBought: 3
  }
];
