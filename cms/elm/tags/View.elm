module Tags.View exposing (..)

import Types exposing (..)
import State exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput, onClick, onCheck)


view : Model -> Html Msg
view model =
    div [ class "overflow-hidden ph4 ph3-m ph3-l" ]
        [ div [ class ("w-200 relative center " ++ (getPosition model.position)) ]
            [ render_filter_block 1 model.issue_label model.issue_tags model.selected_tags "mr-5"
            , render_filter_block 2 model.reason_label model.reason_tags model.selected_tags "mr-5"
            , render_filter_block 3 model.content_label model.content_tags model.selected_tags ""
            ]
        ]


render_filter_block : Int -> String -> List String -> List Tag -> String -> Html Msg
render_filter_block num filter_label tags selected_tags classname =
    div [ class ("br1 shadow-2 w-30 tl pa3 mb3 dib " ++ classname) ]
        ([ h3 [ class "ma0" ] [ text ("Q" ++ (toString num) ++ " of 3") ]
         , h4 [ class "w-70 mv3" ] [ text filter_label ]
         ]
            ++ (List.map (\t -> render_tag_list t selected_tags num) tags)
            ++ [ div []
                    [ div [ class "w-50 tl dib" ] [ button [ onClick (ChangePosition (num - 1)) ] [ text "previous question" ] ]
                    , div [ class "w-50 tr dib" ] [ button [ onClick (ChangePosition (num + 1)) ] [ text "next question" ] ]
                    ]
               ]
        )


render_tag_list : String -> List Tag -> Int -> Html Msg
render_tag_list tag selected_tags num =
    div [ class "dib" ]
        [ button
            [ class ("b--lm-orange ba br2 ph2 pv1 lh-tag dib mb1 pointer font nunito " ++ (getTagColour (create_tag num tag) selected_tags))
            , onClick (SelectTag (create_tag num tag))
            ]
            [ text tag ]
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


getTagColour : Tag -> List Tag -> String
getTagColour tag selected_tags =
    if List.member tag selected_tags then
        "lm-bg-orange-70"
    else
        "lm-bg-orange-20"


create_tag : Int -> String -> Tag
create_tag num name =
    case num of
        1 ->
            Tag "issue" name

        2 ->
            Tag "reason" name

        3 ->
            Tag "content" name

        _ ->
            Tag "issue" name
