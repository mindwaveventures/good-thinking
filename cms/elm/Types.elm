module Types exposing (..)


type alias Flags =
    { issue_tags : List String
    , reason_tags : List String
    , content_tags : List String
    }


type alias Model =
    { issue_tags : List String
    , reason_tags : List String
    , content_tags : List String
    , position : Int
    }


type Msg
    = ChangePosition Int
