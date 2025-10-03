import React from 'react'
import { motion } from 'framer-motion'
import { mockNews } from '@/data/mockData'

function NewsPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Latest News
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Stay updated with the latest news and announcements from Bellandur Cricket League
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {mockNews.map((article, index) => (
            <motion.article
              key={article.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="group"
            >
              <div className="card card-hover h-full">
                <div className="aspect-video bg-gradient-to-br from-primary-green to-primary-green-800 rounded-lg mb-4 overflow-hidden">
                  <div className="w-full h-full flex items-center justify-center">
                    <span className="material-icons text-white text-4xl">article</span>
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center space-x-2 text-sm text-gray-500">
                    <span className="material-icons text-base">person</span>
                    <span>{article.author}</span>
                    <span>•</span>
                    <span>{new Date(article.publishedAt).toLocaleDateString()}</span>
                  </div>

                  <h3 className="text-xl font-bold text-gray-900 group-hover:text-primary-green transition-colors duration-200">
                    {article.title}
                  </h3>

                  <p className="text-gray-600">
                    {article.excerpt}
                  </p>

                  <div className="flex items-center justify-between pt-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      article.category === 'announcement' 
                        ? 'bg-blue-100 text-blue-800'
                        : article.category === 'match-report'
                        ? 'bg-primary-green-100 text-primary-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {article.category.replace('-', ' ').toUpperCase()}
                    </span>
                  </div>
                </div>
              </div>
            </motion.article>
          ))}
        </div>
      </div>
    </div>
  )
}

export default NewsPage
