module Tips.View exposing (..)

import Types exposing (..)
import State exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput, onClick, onCheck)
import Json.Encode


view : Model -> List String -> String -> Html Msg
view model tips classname =
    case List.length tips of
        0 ->
            div [ class "dn" ] []

        1 ->
            case List.head tips of
                Just tip ->
                    tip_view model 0 tip ("w-60-ns center " ++ classname)

                Nothing ->
                    div [] []

        2 ->
            div
                [ class "overflow-hidden" ]
                [ div [ class (classname ++ " tag-container w-200-ns w-330 relative center " ++ (getPosition model.tip_position)) ]
                    (List.indexedMap (\i el -> tip_view model i el "dib w-30 mr-1p-ns mr-1p") tips)
                ]

        _ ->
            div [ class "overflow-hidden" ]
                [ div [ class ("tag-container w-200-ns w-330 relative center " ++ (getPositionThree model.tip_position)) ]
                    (List.indexedMap (\i el -> tip_view model i el ("dib w-30 mr-1p-ns mr-1p " ++ classname)) tips)
                ]


tip_view : Model -> Int -> String -> String -> Html Msg
tip_view model index page classname =
    div
        [ onClick
            (if (model.tag_position == (index + 1)) then
                NoOp
             else
                (ChangePosition (index + 1))
            )
        , property "innerHTML" (Json.Encode.string page)
        , class classname
        ]
        []


getPosition : Int -> String
getPosition pos =
    case pos of
        1 ->
            "r-18-ns r-0"

        2 ->
            "r-80-ns r-102"

        _ ->
            "r-18-ns"


getPositionThree : Int -> String
getPositionThree pos =
    case pos of
        1 ->
            "l-13-ns r-0"

        2 ->
            "r-49-ns r-102"

        3 ->
            "r-111-ns r-204"

        _ ->
            "l-13-ns"
