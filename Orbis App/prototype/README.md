# Orbis

A prototype for communication, identity and protection in one app. This
repository contains a zero-dependency Python backend that serves the static
front-end and stores application state in SQLite behind a small JSON REST API.

> Prototype: all data is mock/demo data. There are no security, privacy or
> legal guarantees. Do not use with real personal, financial or confidential
> information.

## Quick start

Requirements: Python 3 (standard library only, no `pip install` needed).

```
python server.py
```

Or on Windows, double-click `start.bat` (it runs `python server.py`).

The server prints its URL and opens your browser automatically:

```
http://127.0.0.1:8765/
```

Options:

| Flag           | Default     | Description                          |
| -------------- | ----------- | ------------------------------------ |
| `--port N`     | `8765`      | Port to listen on                    |
| `--host H`     | `127.0.0.1` | Host/interface to bind               |
| `--no-browser` | off         | Do not open a browser on start       |

Examples:

```
python server.py --port 9000
python server.py --port 8766 --no-browser
```

## Local mode (opens without a server)

`app.html` is fully self-contained and works when opened directly from the
filesystem (`file://`). Double-click `app.html` to use it offline. Because the
API sends permissive CORS headers (`Access-Control-Allow-Origin: *`), a page
opened from `file://` can still talk to a running `server.py` if needed.

## API reference

Base path: `/api`. All API responses are UTF-8 JSON
(`Content-Type: application/json`). Errors use `{"error":"<message>"}`.

| Method | Path                | Description                                            |
| ------ | ------------------- | ------------------------------------------------------ |
| GET    | `/api/health`       | Liveness probe: `{"status":"ok","app":"orbis","version":"1.0"}` |
| GET    | `/api/state`        | One object with every collection as a top-level key    |
| GET    | `/api/<collection>` | Stored JSON value for a collection (404 if unknown)    |
| PUT    | `/api/<collection>` | Replace a collection's value; appends an audit event   |
| GET    | `/api/audit`        | Audit events, newest first                             |
| POST   | `/api/audit`        | Append an event `{"actor","action","object"}`          |
| GET    | `/api/export`       | Full state as a downloadable JSON attachment           |
| POST   | `/api/reset`        | Delete and reseed all collections                      |
| OPTIONS| any `/api/*`        | CORS preflight (`204`)                                 |

Collections: `queue`, `commitments`, `aura`, `culture`, `growth`, `sources`,
`audit`, `settings`, `work`.

`PUT /api/<collection>` responds with:

```json
{ "ok": true, "collection": "<name>", "value": <saved value> }
```

Every successful `PUT` appends this event to the audit log:

```json
{ "actor": "you", "action": "update", "object": "<collection>", "time": "<ISO 8601>" }
```

### Quick examples

```
curl http://127.0.0.1:8765/api/health
curl http://127.0.0.1:8765/api/state
curl -X PUT http://127.0.0.1:8765/api/settings -H "Content-Type: application/json" -d "{\"quietHours\":false,\"aiPaused\":false,\"theme\":\"dark\"}"
curl -X POST http://127.0.0.1:8765/api/audit -H "Content-Type: application/json" -d "{\"actor\":\"you\",\"action\":\"reviewed\",\"object\":\"queue\"}"
curl -X POST http://127.0.0.1:8765/api/reset
```

## Storage model

One SQLite table keeps everything:

```sql
CREATE TABLE store (collection TEXT PRIMARY KEY, value TEXT NOT NULL);
```

Each `value` is a JSON document. The database lives at `data/orbis.db` and is
created and seeded automatically on first run. Set the `ORBIS_DB` environment
variable to point at a different file (used by the test suite for isolation).

## File map

| Path                     | Purpose                                                     |
| ------------------------ | ----------------------------------------------------------- |
| `server.py`              | Stdlib HTTP server, SQLite persistence, JSON API, static serving |
| `data/orbis.db`          | SQLite database (created automatically at runtime)          |
| `index.html`             | Landing page (owned elsewhere; not modified here)           |
| `app.html`               | Main app UI, self-contained (owned elsewhere; not modified) |
| `manifest.webmanifest`   | PWA manifest                                                |
| `sw.js`                  | Service worker (network-first HTML, cache-first static)     |
| `icons/orbit.svg`        | Orbit logo (`#4338CA`)                                      |
| `start.bat`              | Windows launcher                                            |
| `tests/verify_api.py`    | Stdlib end-to-end API test (spawns its own server)          |
| `README.md`              | This file                                                   |

## Architecture

- `ThreadingHTTPServer` handles requests concurrently (`BaseHTTPRequestHandler`
  subclass).
- SQLite access is guarded by a process-wide lock; each operation uses a short
  lived connection so the handler stays simple and thread safe.
- The API and static files share one process. Unknown paths and the `/data/`
  directory return a JSON 404; path traversal is blocked.
- First run creates the `store` table and seeds it; `POST /api/reset` clears
  and reseeds it.

## Testing

```
python tests/verify_api.py
```

The test spawns its own isolated server instance (temporary database, free
port) and checks health, state, collection GET/PUT round-trip, audit append,
export headers, reset, CORS headers and error handling.

## PWA notes

Serve over `http://127.0.0.1:8765/` and the app is installable. The service
worker registers only on secure contexts (`localhost`/`127.0.0.1` or HTTPS);
opening `app.html` via `file://` bypasses the service worker and runs locally.

## License / disclaimer

Prototype software provided as-is for demonstration. Mock data only. No
warranty. Not audited for security, accessibility or compliance.
