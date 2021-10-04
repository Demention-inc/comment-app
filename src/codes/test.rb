
require "fileutils"
require 'json'


name="L3lczgH2VqI"



File.foreach("../hash_data/"+name+".rb") do |line|
  config = eval line
  if config["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]!=nil then
    p config["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]
  elsif config["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatPaidMessageRenderer"]["timestampText"]["simpleText"]!=nil then
    p config["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatPaidMessageRenderer"]["timestampText"]["simpleText"]
    # p config
  end
  # p config
end
# line={"replayChatItemAction"=>{"actions"=>[{"addChatItemAction"=>{"item"=>{"liveChatPaidMessageRenderer"=>{"id"=>"ChwKGkNJdTd3ZG5hN3U4Q0ZTUVJyUVlkSEo4S1p3", "timestampUsec"=>"1617887000357297", "authorName"=>{"simpleText"=>"らむ"}, "authorPhoto"=>{"thumbnails"=>[{"url"=>"https://yt4.ggpht.com/ytc/AKedOLTY94dwaTrCWU-_Gb_GbXdUrx1S_M7iJeQatw=s32-c-k-c0x00ffffff-no-rj", "width"=>32, "height"=>32}, {"url"=>"https://yt4.ggpht.com/ytc/AKedOLTY94dwaTrCWU-_Gb_GbXdUrx1S_M7iJeQatw=s64-c-k-c0x00ffffff-no-rj", "width"=>64, "height"=>64}]}, "purchaseAmountText"=>{"simpleText"=>"￥610"}, "headerBackgroundColor"=>4278239141, "headerTextColor"=>4278190080, "bodyBackgroundColor"=>4280150454, "bodyTextColor"=>4278190080, "authorExternalChannelId"=>"UCsTM0inFsaksI8NuMo4hKvA", "authorNameTextColor"=>2315255808, "contextMenuEndpoint"=>{"commandMetadata"=>{"webCommandMetadata"=>{"ignoreNavigation"=>true}}, "liveChatItemContextMenuEndpoint"=>{"params"=>"Q2g0S0hBb2FRMGwxTjNka2JtRTNkVGhEUmxOUlVuSlJXV1JJU2poTFduY2FLU29uQ2hoVlEyMTVlbW81WnpORFUybEZZbVpQU1UxTlFYcFBhMmNTQzB3emJHTjZaMGd5Vm5GSklBRW9CRElhQ2hoVlEzTlVUVEJwYmtaellXdHpTVGhPZFUxdk5HaExka0UlM0Q="}}, "timestampColor"=>2147483648, "contextMenuAccessibility"=>{"accessibilityData"=>{"label"=>"コメントの操作"}}, "timestampText"=>{"simpleText"=>"1:08"}}}}}], "videoOffsetTimeMsec"=>"68670"}}