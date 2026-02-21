port        ENV.fetch("PORT", 8080)
environment ENV.fetch("RACK_ENV", "development")
workers     ENV.fetch("WEB_CONCURRENCY", 2)
threads     1, 3

preload_app!
