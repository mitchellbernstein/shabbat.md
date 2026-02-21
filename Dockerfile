FROM ruby:3.3-slim

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Gemfile Gemfile.lock ./
RUN bundle install --without development test

COPY . .

EXPOSE 8080

ENV RACK_ENV=production
ENV PORT=8080

CMD ["bundle", "exec", "puma", "-C", "config/puma.rb"]
