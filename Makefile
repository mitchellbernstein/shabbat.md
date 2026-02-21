.PHONY: build deploy dev

# Render the Sinatra app to docs/index.html and push to GitHub
deploy: build
	@git add docs/index.html
	@git diff --cached --quiet || git commit -m "Rebuild static site"
	@git push
	@echo "✓ Deployed to GitHub Pages"

# Re-render docs/index.html from the running Sinatra app (or start one temporarily)
build:
	@if lsof -ti:8080 > /dev/null 2>&1; then \
		echo "→ Server already running, rendering..."; \
		curl -s http://localhost:8080 > docs/index.html; \
		echo "✓ docs/index.html updated"; \
	else \
		echo "→ Starting server..."; \
		bundle exec ruby app.rb > /tmp/sinatra-build.log 2>&1 & \
		SERVER_PID=$$!; \
		sleep 2; \
		curl -s http://localhost:8080 > docs/index.html; \
		kill $$SERVER_PID 2>/dev/null; \
		echo "✓ docs/index.html updated"; \
	fi

# Run the local dev server
dev:
	@bundle exec ruby app.rb
