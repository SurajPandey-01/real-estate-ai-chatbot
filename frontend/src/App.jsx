import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'
const API_URL = import.meta.env.VITE_API_URL || '/api/chat';

function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content:
        "Hello! Welcome to EstateAI. I can help you explore properties and projects from DarGlobal and Wasalt. What are you looking for today?",
      sources: [],
    },
  ])

  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const suggestions = [
    'Which villa projects are available in Dubai?',
    'Show me properties in Riyadh',
    'What is the price of the Wasalt property?',
  ]

  const sendMessage = async (text = input) => {
    const question = text.trim()

    if (!question || loading) return

    setMessages((previous) => [
      ...previous,
      { role: 'user', content: question, sources: [] },
    ])

    setInput('')
    setLoading(true)

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: question }),
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      const data = await response.json()

      setMessages((previous) => [
        ...previous,
        {
          role: 'assistant',
          content: data.answer,
          sources: data.sources || [],
        },
      ])
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: 'assistant',
          content:
            'Sorry, I could not connect to the server. Please make sure the backend is running and try again.',
          sources: [],
        },
      ])

      console.error('Chat error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">E</div>
          <div>
            <h2>EstateAI</h2>
            <span>PROPERTY ASSISTANT</span>
          </div>
        </div>

        <button
          className="new-chat"
          onClick={() =>
            setMessages([
              {
                role: 'assistant',
                content: 'Hello! What property information can I help you find?',
                sources: [],
              },
            ])
          }
        >
          + New conversation
        </button>

        <div className="sidebar-section">
          <p className="section-label">DATA SOURCES</p>

          <div className="source-item">
            <span className="source-dot wasalt-dot"></span>
            <div>
              <strong>Wasalt</strong>
              <small>Saudi Arabia properties</small>
            </div>
          </div>

          <div className="source-item">
            <span className="source-dot darglobal-dot"></span>
            <div>
              <strong>DarGlobal</strong>
              <small>Luxury developments</small>
            </div>
          </div>
        </div>

        <div className="sidebar-footer">
          <span className="online-dot"></span>
          AI Assistant Online
        </div>
      </aside>

      <main className="chat-area">
        <header className="topbar">
          <div>
            <h3>Property Assistant</h3>
            <p>Explore real estate with AI-powered search</p>
          </div>
          <div className="topbar-badge">AI POWERED</div>
        </header>

        <section className="messages-area">
          {messages.map((message, index) => (
            <div
              className={`message-row ${message.role}`}
              key={index}
            >
              <div className="avatar">
                {message.role === 'assistant' ? 'E' : 'Y'}
              </div>

              <div className="message-content">
                <span className="message-author">
                  {message.role === 'assistant' ? 'EstateAI' : 'You'}
                </span>

                <div className="message-bubble">
                  {message.role === 'assistant' ? (
                    <ReactMarkdown
                      components={{
                        a: ({ ...props }) => (
                          <a
                            {...props}
                            target="_blank"
                            rel="noopener noreferrer"
                          />
                        ),
                      }}
                    >
                      {message.content}
                    </ReactMarkdown>
                  ) : (
                    message.content
                  )}
                </div>

                {message.sources?.length > 0 && (
                  <div className="sources">
                    <p>PROPERTY SOURCES</p>

                    {message.sources.map((source, sourceIndex) => (
                      <a
                        href={source.url}
                        target="_blank"
                        rel="noreferrer"
                        className="source-card"
                        key={`${source.url}-${sourceIndex}`}
                      >
                        <div>
                          <strong>{source.name}</strong>
                          <small>{source.source}</small>
                        </div>
                        <span>↗</span>
                      </a>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="typing-indicator">
              EstateAI is thinking...
            </div>
          )}
        </section>

        <section className="chat-bottom">
          {messages.length === 1 && (
            <div className="suggestions">
              <p>TRY ASKING</p>
              <div className="suggestion-list">
                {suggestions.map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => sendMessage(suggestion)}
                  >
                    {suggestion} →
                  </button>
                ))}
              </div>
            </div>
          )}

          <form
            className="chat-input-container"
            onSubmit={(event) => {
              event.preventDefault()
              sendMessage()
            }}
          >
            <input
              type="text"
              placeholder="Ask anything about properties..."
              value={input}
              onChange={(event) => setInput(event.target.value)}
              disabled={loading}
            />

            <button type="submit" disabled={loading || !input.trim()}>
              Send ↑
            </button>
          </form>

          <p className="disclaimer">
            EstateAI uses available property data from Wasalt and DarGlobal.
            Verify listing details with the original source.
          </p>
        </section>
      </main>
    </div>
  )
}

export default App
