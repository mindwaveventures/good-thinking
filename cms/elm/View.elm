module View exposing (..)

import Tags.View as Tags
import Resources.View as Resources
import Types exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)


view : Model -> Html Msg
view model =
    div []
        [ Tags.view model
        , div [ class "pa1 ph4 ph3-m ph3-l" ]
            [ div [ class "w-60-ns center" ]
                [ h3 [ class "tl mt5 nunito" ]
                    [ text ("Showing " ++ (get_num_resources model.resources))
                    ]
                ]
            ]
        , div [ class "pa1 ph4 ph3-m ph3-l pb4 pb5-l" ] (List.map Resources.view model.resources)
        ]


get_num_resources : List String -> String
get_num_resources resources =
    let
        count =
            List.length resources
    in
        if count == 1 then
            (toString count) ++ " resource"
        else
            (toString count) ++ " resources"
