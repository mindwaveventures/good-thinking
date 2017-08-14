module View exposing (..)

import Tags.View as Tags
import Resources.View as Resources
import Types exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput, onClick, onCheck)


view : Model -> Html Msg
view model =
    div []
        [ Tags.view model
        , div [ class "pa1 ph4 ph3-m ph3-l" ]
            [ div [ class "w-60-ns center" ]
                [ div [ class "w-50 dib tl" ]
                    [ h3 [ class "tl mt5 nunito" ]
                        [ text ("Showing " ++ (get_num_resources model.resources))
                        ]
                    ]
                , div [ class "w-50 dib tr" ]
                    [ div [ class "w-80 pv2 b--lm-grey ba pointer tc dib", onClick ToggleOrderBox ]
                        [ h5 [ class "lm-dark-grey pl1 ph2-ns nunito-italic ma0 f5" ]
                            [ span []
                                [ text (get_order_text model.order_by)
                                , span [ class "filter-arrow fa-down nunito lm-orange fr" ]
                                    [ text "▼" ]
                                , span [ class "filter-arrow filter-arrow-hide fa-up nunito lm-orange fr" ]
                                    [ text "▲" ]
                                ]
                            ]
                        , div [ class "w-100 relative" ] [ order_box model.order_box_visible ]
                        ]
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


order_box visible =
    if visible then
        div [ class "absolute bg-white z-100 w-100 mt1 bb bl br b--lm-grey" ]
            [ div [ class "pv3 bb b--lm-grey", onClick (UpdateOrder "relevance") ] [ text "Most Relevant" ]
            , div [ class "pv3", onClick (UpdateOrder "recommended") ] [ text "Most Recommended" ]
            ]
    else
        div [] []


get_order_text : String -> String
get_order_text order =
    case order of
        "relevance" ->
            "Most Relevant"

        "recommended" ->
            "Most Recommended"

        _ ->
            "Order By..."
