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
                [ div [ class "w-50-ns dib-ns tl" ]
                    [ h3 [ class "tl mt5 nunito" ]
                        [ text ("Showing " ++ (get_num_resources model.resources))
                        ]
                    ]
                , div [ class "w-50-ns dib-ns tr-ns tc" ]
                    [ div [ class "w-40 tl tc-ns dib" ] [ h4 [ class "pl1 ph2-ns nunito ma0 mr3 mr1-ns f5 dib ttu" ] [ text "Order By" ] ]
                    , div [ class "w-60 tl dib" ]
                        [ div [ class "w-100 relative dib" ]
                            [ div [ class "w-100 pv2 b--lm-grey ba pointer tc", onClick ToggleOrderBox ]
                                [ h5 [ class "pl1 ph2-ns nunito ma0 f5" ]
                                    [ span []
                                        [ text (get_order_text model.order_by)
                                        , span [ class "filter-arrow fa-down nunito lm-orange fr" ]
                                            [ text "▼" ]
                                        , span [ class "filter-arrow filter-arrow-hide fa-up nunito lm-orange fr" ]
                                            [ text "▲" ]
                                        ]
                                    ]
                                ]
                            , order_box model.order_box_visible
                            ]
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
        div [ class "absolute bg-white z-100 w-100 left-0 bb bl br b--lm-grey tc pointer" ]
            [ div [ class "pv3 bb b--lm-grey", onClick (CloseAndUpdate "relevance") ] [ text "Most Relevant" ]
            , div [ class "pv3", onClick (CloseAndUpdate "recommended") ] [ text "Most Recommended" ]
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
            "Most Relevant"
