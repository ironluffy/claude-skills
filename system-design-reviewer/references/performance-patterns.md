# Performance Optimization Patterns

Quick reference for performance optimization.

## Caching Strategy

### Application-Level Caching (Redis/Memcached)

```python
# Cache frequently accessed data
cache_key = f"user:{user_id}"
user = cache.get(cache_key)
if not user:
    user = database.query(User).get(user_id)
    cache.set(cache_key, user, ttl=300)  # 5 min TTL
```

**When to use**: Frequently read data, expensive computations, session storage

### Database Query Caching

- **Query Result Caching**: Cache entire query results
- **Query Plan Caching**: PostgreSQL automatically caches prepared statements
- **Materialized Views**: Pre-compute complex aggregations

### HTTP Caching

```http
Cache-Control: public, max-age=3600
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Last-Modified: Wed, 21 Oct 2023 07:28:00 GMT
```

## Database Optimization

### Indexing

```sql
-- Index frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);

-- Composite index for common query patterns
CREATE INDEX idx_user_status_created ON users(status, created_at) WHERE status = 'active';
```

### N+1 Query Prevention

```python
# ❌ Bad: N+1 queries
users = User.query.all()
for user in users:
    print(user.orders)  # Separate query for each user!

# ✅ Good: Eager loading
users = User.query.options(joinedload(User.orders)).all()
for user in users:
    print(user.orders)  # Data already loaded
```

### Connection Pooling

```python
# Configure connection pool
engine = create_engine(
    'postgresql://user:pass@host/db',
    pool_size=20,          # Number of connections to maintain
    max_overflow=10,        # Additional connections if needed
    pool_timeout=30,        # Wait time for available connection
    pool_recycle=3600       # Recycle connections after 1 hour
)
```

## Load Management

### Async Processing

```python
# ❌ Bad: Synchronous email sending blocks response
@app.post("/register")
def register(user_data):
    user = create_user(user_data)
    send_welcome_email(user)  # Blocks for 2-5 seconds!
    return {"id": user.id}

# ✅ Good: Async with message queue
@app.post("/register")
def register(user_data):
    user = create_user(user_data)
    queue.enqueue("send_email", user.id)  # Non-blocking
    return {"id": user.id}
```

### Load Balancing

- **Round Robin**: Simple, equal distribution
- **Least Connections**: Route to server with fewest active connections
- **IP Hash**: Sticky sessions based on client IP
- **Weighted**: Distribute based on server capacity

## Response Time Targets

- **Fast**: <100ms - Cached data, simple queries
- **Acceptable**: 100-500ms - Database queries, API calls
- **Slow**: 500ms-1s - Complex operations, multiple external calls
- **Too Slow**: >1s - Needs optimization or async processing

## Compression

```nginx
# Enable gzip compression in nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
gzip_min_length 1000;
gzip_comp_level 6;
```

**Savings**: 60-80% reduction in payload size for text-based content

## CDN Configuration

Serve static assets from CDN:
- **Images**: jpg, png, svg, webp
- **Styles**: css
- **Scripts**: js
- **Fonts**: woff, woff2, ttf

**Benefits**: 30-70% faster loading, reduced origin server load
