# Here Server

A Python-based server for the "Here" road trip companion app. The server handles geospatial POI (Point of Interest) queries, manages a database of interesting locations, and provides text-to-speech audio narration on demand.

## Vision

As users drive on road trips, the companion mobile app periodically sends location updates to this server. The server identifies nearby points of interest, returns teasers, and streams TTS audio narration when requested. Think of it as a knowledgeable local guide riding along, pointing out interesting things you'd otherwise drive right past.

## Core Features

### API Endpoints

- **`POST /nearby`** - Accepts lat/lon coordinates, returns list of nearby POIs with teaser text
- **`GET /poi/{id}`** - Returns full details for a specific POI
- **`GET /audio/{id}`** - Streams TTS audio narration for a POI (generates on-demand or serves cached)
- **`GET /categories`** - Returns available POI categories for filtering

### POI Database

SQLite database with PostGIS-style geospatial indexing (via SpatiaLite or custom R-tree). Each POI record includes:

- Unique ID
- Category (historical_marker, landmark, scenic_overlook, etc.)
- Coordinates (lat/lon)
- Teaser text (short, shown in notification)
- Full description (narrated via TTS)
- Source attribution
- Metadata (date added, last verified, external IDs)

### TTS Generation

- Primary: Edge TTS (free, high quality, multiple voices)
- Audio caching: Pre-generate for popular POIs, on-demand for others
- Format: MP3 for broad compatibility and streaming

### Data Ingestion Tools

Command-line tools and scripts to populate the POI database from various sources:

- **NC Historical Markers** - Initial dataset, scrape/parse from public sources
- Expandable architecture for adding new POI types

## Technology Stack

- **Web Framework**: FastAPI (async, good for streaming audio)
- **Database**: SQLite + SpatiaLite extension (or R-tree index for geo queries)
- **TTS**: edge-tts library
- **Audio**: pydub for any audio processing needs
- **HTTP Client**: httpx or aiohttp for async data fetching
- **CLI Tools**: Click or Typer for data management commands

## Project Structure

```
here-server/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app, CORS, middleware
│   │   ├── routes/
│   │   │   ├── nearby.py     # Location-based POI queries
│   │   │   ├── poi.py        # Individual POI details
│   │   │   └── audio.py      # TTS streaming endpoint
│   │   └── models.py         # Pydantic request/response models
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py       # DB connection, session management
│   │   ├── models.py         # SQLAlchemy/raw SQL models
│   │   └── geo.py            # Geospatial query helpers
│   ├── tts/
│   │   ├── __init__.py
│   │   ├── generator.py      # Edge TTS wrapper
│   │   └── cache.py          # Audio file caching logic
│   └── ingest/
│       ├── __init__.py
│       ├── base.py           # Base ingester class
│       └── nc_historical.py  # NC Historical Markers ingester
├── tools/
│   ├── ingest_cli.py         # CLI for running data ingestion
│   ├── db_cli.py             # CLI for database management
│   └── audio_cli.py          # CLI for pre-generating audio
├── data/
│   ├── here.db               # SQLite database
│   └── audio_cache/          # Cached TTS audio files
├── tests/
├── requirements.txt
├── project.md
└── README.md
```

## Initial POI Source: NC Historical Markers

North Carolina has ~1,600+ historical markers. Data sources to investigate:

- NC Office of Archives and History official list
- ncmarkers.com or similar aggregator sites
- Wikipedia lists of NC historical markers
- OpenStreetMap tagged historical markers

Each marker typically has:
- Marker ID (e.g., "A-1")
- Title
- Inscription text
- Location (often intersection-based, needs geocoding)
- County
- Year erected

## API Design Details

### POST /nearby

```json
// Request
{
  "lat": 35.7796,
  "lon": -78.6382,
  "radius_miles": 5,
  "categories": ["historical_marker"],  // optional filter
  "limit": 10
}

// Response
{
  "pois": [
    {
      "id": "nc-hist-A42",
      "category": "historical_marker",
      "title": "Battle of Bentonville",
      "teaser": "Site of the largest Civil War battle fought in North Carolina...",
      "distance_miles": 0.3,
      "lat": 35.7801,
      "lon": -78.6390
    }
  ]
}
```

### GET /audio/{id}

- Returns audio/mpeg stream
- Supports HTTP Range requests for seeking
- Query param `?voice=en-US-GuyNeural` to select voice
- Generates on-demand if not cached, caches result

## Development Phases

### Phase 1: Foundation
- [ ] Set up project structure and dependencies
- [ ] Implement SQLite database with geo-indexing
- [ ] Create basic FastAPI app with /nearby endpoint
- [ ] Build NC Historical Markers ingester (start with sample data)

### Phase 2: Audio
- [ ] Integrate Edge TTS generation
- [ ] Implement audio caching layer
- [ ] Create /audio streaming endpoint
- [ ] Build CLI for pre-generating popular POI audio

### Phase 3: Data Enrichment
- [ ] Complete NC Historical Markers ingestion
- [ ] Add geocoding for markers with text-only locations
- [ ] Implement data verification/cleanup tools

### Phase 4: Production Readiness
- [ ] Add rate limiting
- [ ] Implement API key authentication (for app)
- [ ] Set up logging and monitoring
- [ ] Deploy (likely on existing server infrastructure)

### Future POI Categories to Consider
- State/National Parks and trailheads
- Scenic overlooks and viewpoints
- Notable architecture
- Famous filming locations
- Local legends and folklore sites
- Roadside attractions
- Historic battlefields
- Notable graves/cemeteries
- Geological features
- Wildlife viewing areas

## Configuration

Environment variables or config file:
- `DATABASE_PATH` - Path to SQLite database
- `AUDIO_CACHE_DIR` - Directory for cached audio files
- `DEFAULT_TTS_VOICE` - Default Edge TTS voice
- `MAX_NEARBY_RADIUS` - Maximum allowed search radius
- `API_KEY` - For authenticating mobile app requests

## Notes

- Keep teaser text punchy (1-2 sentences) - it shows in a notification while driving
- Full narration should be 30-90 seconds typically (don't distract the driver too long)
- Consider "driving context" - audio should be self-contained, no "as you can see" references
- Prioritize accuracy of coordinates - a POI 100 feet off is frustrating

## Related

- Mobile app: Android-first, separate repository
- Name: "Here" - as in "here's something interesting right here"
