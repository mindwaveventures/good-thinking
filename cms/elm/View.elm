module View exposing (..)

import Tags.View as Tags
import Resources.View as Resources
import Tips.View as Tips
import Types exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput, onClick, onCheck)
import Html.Attributes.Aria as Aria


view : Model -> Html Msg
view model =
    div []
        [ Tags.view model
        , div [ class "pa1 ph3" ]
            [ div [ class "w-60-ns center" ]
                [ div [ class "w-50-ns dib-ns tl" ]
                    [ div [ id "results", class "relative top--3 o-0" ] []
                    , h3 [ class "tl mt5 nunito" ]
                        [ text ("Showing " ++ (get_num_resources model))
                        ]
                    ]
                , div [ class "w-50-ns dib-ns tr-ns" ]
                    [ div [ class "w-40-ns tl tc-ns dib" ] [ h4 [ class "ph2-ns montserrat ma0 mr3 mr1-ns f5 dib ttu" ] [ text "Order By" ] ]
                    , div [ class "w-60-ns tl dib" ]
                        [ div [ class "w-100 relative dib" ]
                            [ div [ class "w-100 pv2 b--lm-dark-turquoise br--top br1 ba pointer tc lm-bg-dark-turquoise-hover", onClick ToggleOrderBox ]
                                [ h5 [ class "pl1 ph2-ns montserrat fw3 lm-dark-turquoise lm-white-hover ma0 f5" ]
                                    [ span []
                                        [ text (get_order_text model.order_by)
                                        , i [ class "fa fa-caret-down ph2", Aria.ariaHidden True ] []
                                        ]
                                    ]
                                ]
                            , order_box model.order_box_visible
                            ]
                        ]
                    ]
                ]
            ]
        , div [ class "pa1 ph3 pb1 pb2-l" ] (get_resources model)
        , div [ class "tc ph4 ph3-m ph3-l" ]
            [ button
                [ onClick (ShowMore True)
                , id "see_more"
                , class
                    ("w-60-ns f5 link dib ph3 pv2 br1 pointer nunito tracked inner-shadow-active lm-white lm-bg-dark-turquoise lm-bg-white-hover lm-dark-turquoise-hover ba b--lm-dark-turquoise "
                        ++ if model.show_more || model.resource_count < 4 then
                            "dn-important"
                           else
                            ""
                    )
                ]
                [ text ("See " ++ toString (model.resource_count - 3) ++ " More Resources") ]
            ]
        ]


get_num_resources : Model -> String
get_num_resources model =
    let
        count =
            model.resource_count
    in
        if count == 1 then
            (toString count) ++ " resource"
        else
            (toString count) ++ " resources"


order_box visible =
    if visible then
        div [ class "absolute bg-white z-100 w-100 left-0 br1 bb bl br b--lm-dark-turquoise tc pointer" ]
            [ div [ class "pv3 bb b--lm-dark-turquoise lm-dark-turquoise lm-bg-dark-turquoise-hover lm-white-hover", onClick (CloseAndUpdate "relevance") ] [ text "Most Relevant" ]
            , div [ class "pv3 lm-dark-turquoise lm-bg-dark-turquoise-hover lm-white-hover", onClick (CloseAndUpdate "recommended") ] [ text "Most Recommended" ]
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


get_resources : Model -> List (Html Msg)
get_resources model =
    List.indexedMap
        (\i el ->
            case model.show_more of
                False ->
                    if i < 2 then
                        Resources.view el ""
                    else if (rem (i + 1) 3) == 0 && (i < 3) then
                        div []
                            ([ Tips.view model (List.take 3 (List.drop (i - 3) model.tips)) "" ]
                                ++ [ Resources.view el "" ]
                            )
                    else if (rem (i + 1) 3) == 0 then
                        div []
                            ([ Tips.view model (List.take 3 (List.drop (i - 3) model.tips)) "dn" ]
                                ++ [ Resources.view el "dn" ]
                            )
                    else
                        Resources.view el "dn"

                True ->
                    if (rem (i + 1) 3) == 0 then
                        div []
                            ([ Tips.view model (List.take 3 (List.drop (i - 3) model.tips)) "" ]
                                ++ [ Resources.view el "" ]
                            )
                    else
                        Resources.view el ""
        )
        model.resources


split : Int -> List a -> List (List a)
split i list =
    case List.take i list of
        [] ->
            []

        listHead ->
            listHead :: split i (List.drop i list)
