module View exposing (..)

import Types exposing (..)
import State exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput, onClick, onCheck)


view : Model -> Html Msg
view model =
    div [ class "overflow-hidden ph4 ph3-m ph3-l" ]
        [ div [ class ("w-200 relative center " ++ (getPosition model.position)) ]
            [ render_filter_block 1 "what is your issue?" model.issue_tags "mr-5"
            , render_filter_block 2 "what is your reason?" model.reason_tags "mr-5"
            , render_filter_block 3 "what is your content?" model.content_tags ""
            ]
        ]


render_filter_block : Int -> String -> List String -> String -> Html Msg
render_filter_block num filter_label tags classname =
    div [ class ("br1 shadow-2 w-30 tl pa3 mb3 dib " ++ classname) ]
        ([ h3 [ class "ma0" ] [ text ("Q" ++ (toString num) ++ " of 3") ]
         , h4 [ class "w-70 mv3" ] [ text filter_label ]
         ]
            ++ (List.map render_tag_list tags)
            ++ [ div []
                    [ div [ class "w-50 tl dib" ] [ button [ onClick (ChangePosition (num - 1)) ] [ text "previous question" ] ]
                    , div [ class "w-50 tr dib" ] [ button [ onClick (ChangePosition (num + 1)) ] [ text "next question" ] ]
                    ]
               ]
        )


render_tag_list : String -> Html Msg
render_tag_list tag =
    div [ class "dib" ]
        [ button [ class "b--lm-orange lm-bg-orange-20 ba br2 ph2 pv1 lh-tag dib mb1 pointer font nunito" ] [ text tag ]
        ]


getPosition : Int -> String
getPosition pos =
    case pos of
        1 ->
            "l-20"

        2 ->
            "r-50"

        3 ->
            "r-120"

        _ ->
            "l-20"
