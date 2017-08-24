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
    , order : String
    , search : String
    , page : String
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
    , order_box_visible : Bool
    , order_by : String
    , search : String
    , show_more : Bool
    , page : String
    }


type alias Tag =
    { tag_type : String
    , name : String
    }


type Msg
    = NoOp
    | ChangePosition Int
    | SelectTag Tag
    | QueryComplete (Result Http.Error (List String))
    | GetData String
    | ToggleOrderBox
    | UpdateOrder String
    | CloseAndUpdate String
    | UpdateTags (List Tag)
    | Swipe String
    | ShowMore Bool
