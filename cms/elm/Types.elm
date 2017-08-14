module Types exposing (..)

import Http


type alias Flags =
    { issue_tags : List String
    , reason_tags : List String
    , content_tags : List String
    , issue_label : String
    , content_label : String
    , reason_label : String
    , selected_tags : List Tag
    , query : String
    }


type alias Model =
    { issue_tags : List String
    , reason_tags : List String
    , content_tags : List String
    , issue_label : String
    , content_label : String
    , reason_label : String
    , selected_tags : List Tag
    , position : Int
    , resources : List String
    }


type alias Tag =
    { tag_type : String
    , name : String
    }


type Msg
    = ChangePosition Int
    | SelectTag Tag
    | QueryComplete (Result Http.Error (List String))
    | GetData String
