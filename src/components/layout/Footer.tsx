import React from 'react'
import { Link } from '@tanstack/react-router'
import { motion } from 'framer-motion'

function Footer() {
  const currentYear = new Date().getFullYear()

  const footerSections = [
    {
      title: 'TEAM',
      links: [
        { label: 'MR Titans', href: '/teams/mr-titans' },
        { label: 'Bellandur Monsters', href: '/teams/bellandur-monsters' },
        { label: 'Y K R Cricketers', href: '/teams/ykr-cricketers' },
        { label: 'Bellandur Sharks Cricketers', href: '/teams/bellandur-sharks' },
        { label: 'Super Giants Bellandur', href: '/teams/super-giants-bellandur' },
        { label: 'Royal Changlesrs Bellandur', href: '/teams/royal-changlesrs-bellandur' }
      ]
    },
    {
      title: 'ABOUT',
      links: [
        { label: 'About Us', href: '/about' },
        { label: 'Anti Corruption Code', href: '/about/anti-corruption' },
        { label: 'Anti Doping Rules', href: '/about/anti-doping' },
        { label: 'Code Of Conduct', href: '/about/code-of-conduct' },
        { label: 'News Access Regulations', href: '/about/news-access' },
        { label: 'Image Use Terms', href: '/about/image-use' }
      ]
    },
    {
      title: 'GUIDELINES',
      links: [
        { label: 'IPL Code Of Conduct', href: '/guidelines/conduct' },
        { label: 'Brand Guidelines', href: '/guidelines/brand' },
        { label: 'Governing Council', href: '/guidelines/governing-council' },
        { label: 'Match Playing Conditions', href: '/guidelines/playing-conditions' },
        { label: 'PMOA Standards', href: '/guidelines/pmoa' },
        { label: 'Suspect Action Policy', href: '/guidelines/suspect-action' }
      ]
    },
    {
      title: 'CONTACT',
      links: [
        { label: 'Contact Us', href: '/contact' },
        { label: 'Sponsorship', href: '/contact/sponsorship' },
        { label: 'Privacy Policy', href: '/privacy' },
        { label: 'Terms & Conditions', href: '/terms' }
      ]
    }
  ]

  const sponsors = [
    { name: 'TATA', logo: '/images/sponsors/tata.png', category: 'title' },
    { name: 'My11Circle', logo: '/images/sponsors/my11circle.png', category: 'associate' },
    { name: 'AngelOne', logo: '/images/sponsors/angelone.png', category: 'associate' },
    { name: 'RuPay', logo: '/images/sponsors/rupay.png', category: 'associate' },
    { name: 'Wonder Cement', logo: '/images/sponsors/wonder-cement.png', category: 'umpire' },
    { name: 'CEAT', logo: '/images/sponsors/ceat.png', category: 'timeout' }
  ]

  return (
    <footer className="bg-cricket-dark text-white">
      {/* Main Footer Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {footerSections.map((section, index) => (
            <motion.div
              key={section.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <h3 className="text-lg font-semibold mb-4 text-cricket-gold">
                {section.title}
              </h3>
              <ul className="space-y-2">
                {section.links.map((link) => (
                  <li key={link.href}>
                    <Link
                      to={link.href}
                      className="text-gray-300 hover:text-cricket-gold transition-colors duration-200 text-sm"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>

        {/* Sponsors Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-12 pt-8 border-t border-gray-700"
        >
          <h3 className="text-lg font-semibold mb-6 text-cricket-gold text-center">
            Our Partners
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 items-center">
            {sponsors.map((sponsor, index) => (
              <motion.div
                key={sponsor.name}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className="flex items-center justify-center p-4 bg-white rounded-lg hover:shadow-lg transition-shadow duration-300"
              >
                <img
                  src={sponsor.logo}
                  alt={sponsor.name}
                  className="h-8 w-auto object-contain"
                />
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Social Media Links */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-8 pt-8 border-t border-gray-700 text-center"
        >
          <div className="flex justify-center space-x-6 mb-4">
            <a
              href="#"
              className="text-gray-300 hover:text-cricket-gold transition-colors duration-200"
              aria-label="Facebook"
            >
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
            </a>
            <a
              href="#"
              className="text-gray-300 hover:text-cricket-gold transition-colors duration-200"
              aria-label="Twitter"
            >
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
              </svg>
            </a>
            <a
              href="#"
              className="text-gray-300 hover:text-cricket-gold transition-colors duration-200"
              aria-label="Instagram"
            >
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 6.62 5.367 11.987 11.988 11.987s11.987-5.367 11.987-11.987C24.014 5.367 18.647.001 12.017.001zM8.449 16.988c-1.297 0-2.448-.49-3.323-1.297C4.198 14.895 3.708 13.744 3.708 12.447s.49-2.448 1.297-3.323c.875-.807 2.026-1.297 3.323-1.297s2.448.49 3.323 1.297c.807.875 1.297 2.026 1.297 3.323s-.49 2.448-1.297 3.323c-.875.807-2.026 1.297-3.323 1.297z"/>
              </svg>
            </a>
            <a
              href="#"
              className="text-gray-300 hover:text-cricket-gold transition-colors duration-200"
              aria-label="YouTube"
            >
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
              </svg>
            </a>
          </div>
        </motion.div>
      </div>

      {/* Copyright */}
      <div className="bg-black py-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-400 text-sm">
            Copyright © BCL {currentYear} All Rights Reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
