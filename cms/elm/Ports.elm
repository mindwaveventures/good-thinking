port module Ports exposing (..)

import Types exposing (Tag)


port listeners : () -> Cmd msg


port selectTag : Tag -> Cmd msg


port changeOrder : String -> Cmd msg


port updateTags : (List Tag -> msg) -> Sub msg


port swipe : (String -> msg) -> Sub msg


port tipSwipe : (String -> msg) -> Sub msg


port clickScroll : () -> Sub msg
