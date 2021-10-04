require "fileutils"
require 'json'
require 'csv'


name=ARGV[0]

FileUtils.cp("../txt/"+name+".txt","../hash_data/"+name+".rb")


count = 0
CSV.open('../csv/'+name+'.csv', 'a') do |csvFile|
  csvFile.puts(['id','timestamp'])
  File.foreach("../hash_data/"+name+".rb") do |line|
    config = eval line
    begin   
        if config["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatPaidMessageRenderer"];
          p config["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatPaidMessageRenderer"]["timestampText"]["simpleText"]
          count += 1
          csvFile.puts([count, config["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatPaidMessageRenderer"]["timestampText"]["simpleText"]])
        elsif config["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"];
          p config["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]
          count += 1
          csvFile << [count, config["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]]
        elsif config["replayChatItemAction"]["actions"][0]["addLiveChatTickerItemAction"];
          p config["replayChatItemAction"]["actions"][0]["addLiveChatTickerItemAction"]["item"]["liveChatTickerPaidMessageItemRenderer"]  ["showItemEndpoint"]["showLiveChatItemEndpoint"]["renderer"]["liveChatPaidMessageRenderer"]["timestampText"]["simpleText"]
          count += 1
          csvFile << [count, config["replayChatItemAction"]["actions"][0]["addLiveChatTickerItemAction"]["item"]["liveChatTickerPaidMessageItemRenderer"] ["showItemEndpoint"]["showLiveChatItemEndpoint"]["renderer"]["liveChatPaidMessageRenderer"]["timestampText"]["simpleText"]]
        end
    rescue => e
    end
  end
end