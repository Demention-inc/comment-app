require "fileutils"
require 'json'
require "csv"


name="L3lczgH2VqI"
# name=ARGV[0]
 
FileUtils.cp("../../txt/"+name+".txt","../../hash_data/"+name+".rb")

File.foreach("../../hash_data/"+name+".rb") do |line|
  config = eval line
  k=config.to_json
  
  File.open("../../json/test.json","a") {|file| 
    file.puts(JSON.generate(config))
  }
end


