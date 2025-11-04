export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Navigation */}
      <nav className="border-b border-gray-200 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <span className="text-2xl font-bold text-gray-900">GraphCare</span>
              <span className="ml-2 text-sm text-gray-500">by Mind Protocol</span>
            </div>
            <div className="flex items-center gap-6">
              <a href="#services" className="text-gray-700 hover:text-gray-900">Services</a>
              <a href="#how-it-works" className="text-gray-700 hover:text-gray-900">How It Works</a>
              <a href="#case-study" className="text-gray-700 hover:text-gray-900">Case Study</a>
              <a href="#contact" className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">Get Started</a>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="bg-gradient-to-b from-blue-50 to-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              Transform Your Codebase Into a <span className="text-blue-600">Living Knowledge Graph</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Professional knowledge extraction service. We transform your code and documentation into a queryable,
              navigable L2 organizational graph using Mind Protocol's universal type system.
            </p>
            <div className="flex justify-center gap-4">
              <a href="#contact" className="bg-blue-600 text-white px-8 py-3 rounded-md text-lg font-semibold hover:bg-blue-700">
                Start Evidence Sprint
              </a>
              <a href="#how-it-works" className="border border-gray-300 text-gray-700 px-8 py-3 rounded-md text-lg font-semibold hover:bg-gray-50">
                Learn More
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Our Services</h2>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Evidence Sprint */}
            <div className="border border-gray-200 rounded-lg p-8 hover:shadow-lg transition-shadow">
              <div className="flex items-center mb-4">
                <div className="bg-blue-100 text-blue-600 rounded-full p-3">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold ml-4">Evidence Sprint</h3>
              </div>
              <p className="text-gray-600 mb-4">
                6-8 hour intensive extraction. We extract your codebase into a complete knowledge graph with semantic search,
                architecture diagrams, coverage analysis, and security audits.
              </p>
              <ul className="space-y-2 mb-6">
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span className="text-gray-700">Complete code extraction (functions, classes, dependencies)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span className="text-gray-700">Semantic clustering (identify themes and patterns)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span className="text-gray-700">Architecture inference (layers, services, patterns)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span className="text-gray-700">Coverage & security analysis</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span className="text-gray-700">Interactive documentation website</span>
                </li>
              </ul>
              <div className="text-3xl font-bold mb-2">~$350 <span className="text-lg font-normal text-gray-500">$MIND</span></div>
              <p className="text-sm text-gray-500 mb-4">One-time extraction, lifetime value</p>
              <a href="#contact" className="block w-full text-center bg-blue-600 text-white py-3 rounded-md font-semibold hover:bg-blue-700">
                Book Evidence Sprint
              </a>
            </div>

            {/* Standard Care */}
            <div className="border border-gray-200 rounded-lg p-8 hover:shadow-lg transition-shadow">
              <div className="flex items-center mb-4">
                <div className="bg-green-100 text-green-600 rounded-full p-3">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold ml-4">Standard Care</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Ongoing health monitoring for your knowledge graph. Automatic drift detection, coverage tracking,
                and continuous quality assurance as your codebase evolves.
              </p>
              <ul className="space-y-2 mb-6">
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span className="text-gray-700">Automated drift detection (code changes monitored)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span className="text-gray-700">Coverage trend analysis (improving or degrading?)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span className="text-gray-700">Security vulnerability alerts</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span className="text-gray-700">Health dashboard (real-time metrics)</span>
                </li>
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span className="text-gray-700">Automatic re-extraction on major changes</span>
                </li>
              </ul>
              <div className="text-3xl font-bold mb-2">Custom <span className="text-lg font-normal text-gray-500">pricing</span></div>
              <p className="text-sm text-gray-500 mb-4">Based on codebase size and update frequency</p>
              <a href="#contact" className="block w-full text-center border border-gray-300 text-gray-700 py-3 rounded-md font-semibold hover:bg-gray-50">
                Contact Us
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="bg-gray-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">How It Works: 11-Stage Extraction Pipeline</h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-blue-600 font-bold text-sm mb-2">STAGE 1-2: CONNECT & PROCESS</div>
              <h3 className="font-bold mb-2">Data Ingestion</h3>
              <p className="text-sm text-gray-600">Clone repositories, parse code, extract documentation with client consent.</p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-blue-600 font-bold text-sm mb-2">STAGE 3: ANALYZE</div>
              <h3 className="font-bold mb-2">Corpus Analysis</h3>
              <p className="text-sm text-gray-600">Semantic clustering, complexity metrics, architecture patterns identified.</p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-blue-600 font-bold text-sm mb-2">STAGE 4-5: STRATEGY</div>
              <h3 className="font-bold mb-2">Approach Selection</h3>
              <p className="text-sm text-gray-600">Code-first vs docs-first strategy based on corpus characteristics.</p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-blue-600 font-bold text-sm mb-2">STAGE 6: EXTRACTION</div>
              <h3 className="font-bold mb-2">Knowledge Graph Build</h3>
              <p className="text-sm text-gray-600">AST parsing, dependency graphs, behavior specs, architecture inference.</p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-blue-600 font-bold text-sm mb-2">STAGE 7-8: HEALTH</div>
              <h3 className="font-bold mb-2">Quality Validation</h3>
              <p className="text-sm text-gray-600">Coverage analysis, security scanning, drift detection, health monitoring.</p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="text-blue-600 font-bold text-sm mb-2">STAGE 9-11: DELIVERY</div>
              <h3 className="font-bold mb-2">Documentation & Delivery</h3>
              <p className="text-sm text-gray-600">Auto-generated docs, human narratives, interactive website deployed.</p>
            </div>
          </div>

          <div className="mt-12 text-center">
            <p className="text-gray-600 mb-4">All graphs use Mind Protocol's universal type system for protocol compatibility</p>
            <div className="flex justify-center gap-2 flex-wrap">
              <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">U4_Code_Artifact</span>
              <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">U4_Knowledge_Object</span>
              <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">U4_Subentity</span>
              <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">U4_IMPLEMENTS</span>
              <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">U4_DOCUMENTS</span>
            </div>
          </div>
        </div>
      </section>

      {/* Case Study Section */}
      <section id="case-study" className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-4">Case Study: Scopelock</h2>
          <p className="text-center text-gray-600 mb-12">Repository access control system - First client extraction</p>

          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-8 md:p-12">
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-bold mb-4">The Challenge</h3>
                <p className="text-gray-700 mb-4">
                  Scopelock had 344 files across Python backend and TypeScript frontend. Documentation existed but was scattered.
                  No single source of truth for architecture, dependencies, or test coverage.
                </p>
                <h3 className="text-xl font-bold mb-4">The Solution</h3>
                <p className="text-gray-700">
                  Complete 6-hour extraction transformed the codebase into a living knowledge graph with semantic search,
                  architecture visualization, and automated quality metrics.
                </p>
              </div>

              <div className="space-y-4">
                <div className="bg-white rounded-lg p-4 shadow-sm">
                  <div className="text-2xl font-bold text-blue-600">344</div>
                  <div className="text-sm text-gray-600">Files extracted & mapped</div>
                </div>
                <div className="bg-white rounded-lg p-4 shadow-sm">
                  <div className="text-2xl font-bold text-green-600">10</div>
                  <div className="text-sm text-gray-600">Architecture themes identified</div>
                </div>
                <div className="bg-white rounded-lg p-4 shadow-sm">
                  <div className="text-2xl font-bold text-purple-600">1.57:1</div>
                  <div className="text-sm text-gray-600">Doc-to-code ratio (well-documented)</div>
                </div>
                <div className="bg-white rounded-lg p-4 shadow-sm">
                  <div className="text-2xl font-bold text-indigo-600">FastAPI + Next.js</div>
                  <div className="text-sm text-gray-600">Architecture pattern detected</div>
                </div>
              </div>
            </div>

            <div className="mt-8 text-center">
              <a
                href="https://docs.scopelock.mindprotocol.ai"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block bg-blue-600 text-white px-6 py-3 rounded-md font-semibold hover:bg-blue-700"
              >
                View Scopelock Knowledge Graph →
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="bg-gray-900 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Codebase?</h2>
          <p className="text-gray-300 mb-8 max-w-2xl mx-auto">
            Book an Evidence Sprint and get your complete knowledge graph in 6-8 hours. No contracts, no subscriptions—just results.
          </p>

          <div className="bg-gray-800 rounded-lg p-8 max-w-md mx-auto">
            <div className="mb-6">
              <div className="text-4xl font-bold mb-2">~$350 <span className="text-xl font-normal text-gray-400">$MIND</span></div>
              <p className="text-gray-400 text-sm">Evidence Sprint • 6-8 hours • Complete extraction</p>
            </div>

            <a
              href="mailto:graphcare@mindprotocol.ai?subject=Evidence%20Sprint%20Inquiry"
              className="block w-full bg-blue-600 text-white py-3 rounded-md font-semibold hover:bg-blue-700 mb-4"
            >
              Email: graphcare@mindprotocol.ai
            </a>

            <p className="text-sm text-gray-400">
              Include: Repository URL, preferred timeline, any specific concerns (security, coverage, architecture)
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <div>
              <span className="text-xl font-bold text-gray-900">GraphCare</span>
              <p className="text-sm text-gray-500 mt-1">By Mind Protocol • L2 Knowledge Extraction Service</p>
            </div>
            <div className="text-sm text-gray-500">
              © 2025 Mind Protocol. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}
