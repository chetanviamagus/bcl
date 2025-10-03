import React from 'react'
import { motion } from 'framer-motion'
import { Link } from '@tanstack/react-router'
import { mockNews } from '@/data/mockData'

function LatestNews() {
  const latestNews = mockNews.slice(0, 3)

  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Latest News
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Stay updated with the latest from Bellandur Cricket League
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {latestNews.map((article, index) => (
            <motion.article
              key={article.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="group"
            >
              <Link to="/news/$newsId" params={{ newsId: article.id }}>
                <div className="card card-hover h-full">
                  {/* Article Image */}
                  <div className="aspect-video bg-gradient-to-br from-primary-green to-primary-green-800 rounded-lg mb-4 overflow-hidden">
                    <div className="w-full h-full flex items-center justify-center">
                      <span className="material-icons text-white text-4xl">article</span>
                    </div>
                  </div>

                  {/* Article Content */}
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2 text-sm text-gray-500">
                      <span className="material-icons text-base">person</span>
                      <span>{article.author}</span>
                      <span>•</span>
                      <span>{new Date(article.publishedAt).toLocaleDateString()}</span>
                    </div>

                    <h3 className="text-xl font-bold text-gray-900 group-hover:text-primary-green transition-colors duration-200 line-clamp-2">
                      {article.title}
                    </h3>

                    <p className="text-gray-600 line-clamp-3">
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
                      
                      <span className="text-primary-green text-sm font-medium group-hover:text-gray-900 transition-colors duration-200">
                        Read More →
                      </span>
                    </div>
                  </div>

                  {/* Hover Effect */}
                  <div className="absolute inset-0 bg-primary-green/5 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
                </div>
              </Link>
            </motion.article>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="text-center mt-12"
        >
          <Link
            to="/news"
            className="btn btn-primary inline-flex items-center"
          >
            <span className="material-icons mr-2">newspaper</span>
            View All News
          </Link>
        </motion.div>
      </div>
    </section>
  )
}

export default LatestNews
