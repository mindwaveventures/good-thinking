module Types exposing (..)

import Http


type alias Flags =
    { issue_tags : List String
    , reason_tags : List String
    , content_tags : List String
    , issue_label : String
    , content_label : String
    , reason_label : String
    , selected_tags : List String
    }


type alias Model =
    { issue_tags : List String
    , reason_tags : List String
    , content_tags : List String
    , issue_label : String
    , content_label : String
    , reason_label : String
    , selected_tags : List String
    , position : Int
    , resources : List String
    }


type Msg
    = ChangePosition Int
    | SelectTag String
    | QueryComplete (Result Http.Error (List String))
    | GetData String
