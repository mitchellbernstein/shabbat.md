require "sinatra"
require "sinatra/reloader" if development?

set :port, ENV.fetch("PORT", 8080)
set :bind, "0.0.0.0"
set :views, File.join(__dir__, "views")
set :public_folder, File.join(__dir__, "public")

get "/" do
  erb :index
end

get "/install" do
  content_type "text/plain"
  send_file File.join(__dir__, "public", "install")
end
