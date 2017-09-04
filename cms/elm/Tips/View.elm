module Tips.View exposing (..)

import Types exposing (..)
import State exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput, onClick, onCheck)
import Json.Encode


view : Model -> Html Msg
view model =
    case List.length model.tips of
        1 ->
            case List.head model.tips of
                Just tip ->
                    tip_view tip ""

                Nothing ->
                    div [] []

        2 ->
            div [ class "overflow-hidden" ]
                [ div [ class ("tag-container w-200-ns w-330 relative center " ++ (getPosition model.tag_position)) ]
                    (List.map (\el -> tip_view el "dib w-30 mr-1p-ns mr-5") model.tips)
                ]

        _ ->
            div [] []


render_tips : Model -> List (Html Msg)
render_tips model =
    List.map (\el -> tip_view el "") model.tips


tip_view : String -> String -> Html Msg
tip_view page classname =
    div [ property "innerHTML" (Json.Encode.string page), class classname ] []


getPosition : Int -> String
getPosition pos =
    case pos of
        1 ->
            "r-18-ns r-0"

        2 ->
            "r-80-ns r-115"

        3 ->
            "r-112-ns r-230"

        _ ->
            "l-12-ns"
