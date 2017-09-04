module Main exposing (main)

import State exposing (..)
import View exposing (..)
import Html


main =
    Html.program
        { init =
            init
                { issue_tags = []
                , reason_tags = []
                , content_tags = []
                , issue_label = ""
                , content_label = ""
                , reason_label = ""
                , selected_tags = []
                , order = ""
                , search = ""
                , page = ""
                }
        , view = view
        , update = update
        , subscriptions = subscriptions
        }
